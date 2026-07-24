"""Central configuration for the Cloud-Connected-Hardware-IoT-Monitor."""

import logging
import os

# ---------------------------------------------------------------------------
# 1. Master JSON schema definition for temperature monitoring
# ---------------------------------------------------------------------------
MONITOR_SCHEMA = {
    "type": "object",
    "required": ["device_id", "timestamp", "temperature", "location"],
    "properties": {
        "device_id": {
            "type": "string",
            "description": "Unique identifier for the IoT sensor device.",
        },
        "timestamp": {
            "type": "string",
            "format": "date-time",
            "description": "ISO-8601 timestamp of the reading.",
        },
        "temperature": {
            "type": "number",
            "description": "Temperature reading in Celsius.",
        },
        "humidity": {
            "type": "number",
            "description": "Relative humidity percentage (0-100).",
        },
        "pressure": {
            "type": "number",
            "description": "Atmospheric pressure in hPa (optional).",
        },
        "location": {
            "type": "object",
            "required": ["room"],
            "properties": {
                "room": {
                    "type": "string",
                    "description": "Server room or location name.",
                },
                "rack_id": {
                    "type": "string",
                    "description": "Rack identifier (optional).",
                },
                "zone": {
                    "type": "string",
                    "description": "Zone within the room (optional).",
                },
            },
        },
        "device_info": {
            "type": "object",
            "properties": {
                "type": {
                    "type": "string",
                    "enum": ["esp32", "raspberry_pi", "arduino"],
                    "description": "Device type.",
                },
                "sensor_type": {
                    "type": "string",
                    "enum": ["dht22", "sht31", "ds18b20", "bme280"],
                    "description": "Sensor model.",
                },
                "firmware_version": {
                    "type": "string",
                    "description": "Firmware version.",
                },
            },
        },
        "status": {
            "type": "string",
            "enum": ["ok", "warning", "critical", "error"],
            "description": "Health status based on temperature thresholds.",
        },
    },
}

# ---------------------------------------------------------------------------
# 2. Temperature threshold constants (Celsius)
# ---------------------------------------------------------------------------
TEMPERATURE_WARNING: float = float(os.getenv("TEMPERATURE_WARNING_THRESHOLD", "28"))
TEMPERATURE_CRITICAL: float = float(os.getenv("TEMPERATURE_CRITICAL_THRESHOLD", "35"))
TEMPERATURE_MIN: float = -10.0
TEMPERATURE_MAX: float = 60.0

# ---------------------------------------------------------------------------
# 3. Azure IoT Hub configuration
# ---------------------------------------------------------------------------
AZURE_IOT_HUB_CONNECTION_STRING: str = os.getenv("AZURE_IOT_HUB_CONNECTION_STRING", "")
AZURE_IOT_HUB_DEVICE_ID: str = os.getenv("AZURE_IOT_HUB_DEVICE_ID", "")

# Fallback to storage account for file-based data exchange
AZURE_STORAGE_ACCOUNT: str = os.getenv("AZURE_STORAGE_ACCOUNT", "")
AZURE_STORAGE_KEY: str = os.getenv("AZURE_STORAGE_KEY", "")
AZURE_FILE_SHARE_NAME: str = os.getenv("AZURE_FILE_SHARE_NAME", "iot-temperature-data")

# ---------------------------------------------------------------------------
# 4. Sensor and polling configuration
# ---------------------------------------------------------------------------
SENSOR_TYPE: str = os.getenv("SENSOR_TYPE", "dht22")
POLL_INTERVAL_SECONDS: int = int(os.getenv("POLL_INTERVAL_SECONDS", "60"))
DATA_RETENTION_DAYS: int = int(os.getenv("DATA_RETENTION_DAYS", "30"))

# ---------------------------------------------------------------------------
# 5. Alert configuration
# ---------------------------------------------------------------------------
ALERT_EMAIL_ENABLED: bool = os.getenv("ALERT_EMAIL_ENABLED", "false").lower() == "true"
ALERT_EMAIL_RECIPIENTS: str = os.getenv("ALERT_EMAIL_RECIPIENTS", "")
ALERT_WEBHOOK_URL: str = os.getenv("ALERT_WEBHOOK_URL", "")

# ---------------------------------------------------------------------------
# 6. Logging configuration
# ---------------------------------------------------------------------------
LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO").upper()
LOG_FORMAT: str = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
LOG_DATE_FORMAT: str = "%Y-%m-%dT%H:%M:%S%z"


def setup_logging() -> None:
    """Configure root logger for the application."""
    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL, logging.INFO),
        format=LOG_FORMAT,
        datefmt=LOG_DATE_FORMAT,
    )
    # Quieten noisy third-party loggers
    logging.getLogger("azure").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("streamlit").setLevel(logging.WARNING)


def get_temperature_status(temp: float) -> tuple[str, str]:
    """
    Get status based on temperature threshold.
    
    Args:
        temp: Temperature in Celsius
        
    Returns:
        Tuple of (status_label, color_name)
    """
    if temp >= TEMPERATURE_CRITICAL:
        return "critical", "red"
    if temp >= TEMPERATURE_WARNING:
        return "warning", "orange"
    return "ok", "green"
