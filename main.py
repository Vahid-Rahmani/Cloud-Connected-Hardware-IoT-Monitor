"""Cloud-Connected-Hardware-IoT-Monitor – application entry point."""

import logging
import os
import signal
import sys
import time
from datetime import datetime, timezone

from monitor.config import (
    AZURE_IOT_HUB_CONNECTION_STRING,
    POLL_INTERVAL_SECONDS,
    SENSOR_TYPE,
    get_temperature_status,
    setup_logging,
)
from monitor.core.alerts import AlertManager
from monitor.core.azure_client import create_azure_client
from monitor.core.sensor import create_sensor
from monitor.utils.formatters import format_reading_summary, format_temperature
from monitor.utils.validators import validate_reading

logger = logging.getLogger(__name__)

# Global flag for graceful shutdown
_running = True


def signal_handler(signum, frame):
    """Handle shutdown signals."""
    global _running
    logger.info("Shutdown signal received")
    _running = False


def run() -> None:
    """Main application entry point."""
    global _running

    setup_logging()
    logger.info("Cloud-Connected-Hardware-IoT-Monitor starting up")

    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Determine if using Azure or local file storage
    use_azure = bool(AZURE_IOT_HUB_CONNECTION_STRING)

    # Initialize components
    sensor_type = os.getenv("SENSOR_TYPE", "simulated")
    sensor = create_sensor(sensor_type=sensor_type)
    client = create_azure_client(use_azure=use_azure)
    alert_manager = AlertManager()

    # Device configuration
    device_id = os.getenv("DEVICE_ID", "sensor-001")
    location = {
        "room": os.getenv("LOCATION_ROOM", "Server Room A"),
        "rack_id": os.getenv("LOCATION_RACK_ID", "Rack-01"),
    }

    logger.info(f"Monitoring started: device={device_id}, sensor={sensor_type}, interval={POLL_INTERVAL_SECONDS}s")

    try:
        while _running:
            try:
                # Read sensor data
                reading_data = sensor.read()

                if reading_data:
                    # Build complete reading
                    reading = {
                        "device_id": device_id,
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                        "temperature": reading_data.get("temperature", 0),
                        "humidity": reading_data.get("humidity"),
                        "location": location,
                        "status": "ok",
                    }

                    # Validate reading
                    try:
                        reading = validate_reading(reading)
                    except Exception as e:
                        logger.warning(f"Reading validation failed: {e}")
                        continue

                    # Check for alerts
                    alert = alert_manager.check_temperature(
                        temperature=reading["temperature"],
                        device_id=device_id,
                        location=location,
                    )

                    if alert:
                        reading["status"] = alert["status"]

                    # Send to Azure or save locally
                    success = client.send_telemetry(reading)

                    if success:
                        summary = format_reading_summary(reading)
                        logger.info(summary)
                    else:
                        logger.warning("Failed to send telemetry")
                else:
                    logger.debug("No sensor data available")

            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")

            # Wait for next reading
            time.sleep(POLL_INTERVAL_SECONDS)

    except KeyboardInterrupt:
        logger.info("Monitoring interrupted by user")
    finally:
        # Cleanup
        sensor.close()
        client.disconnect()
        logger.info("Monitoring stopped")


def run_simulated() -> None:
    """Run with simulated sensor data for testing."""
    logger.info("Running in simulation mode")
    os.environ["SENSOR_TYPE"] = "simulated"
    run()


if __name__ == "__main__":
    # Check for command line arguments
    if len(sys.argv) > 1 and sys.argv[1] == "--simulate":
        run_simulated()
    else:
        run()
