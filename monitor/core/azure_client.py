"""Azure IoT Hub client for sending temperature telemetry."""

import json
import logging
from datetime import datetime, timezone
from typing import Any, Optional

from monitor.config import (
    AZURE_IOT_HUB_CONNECTION_STRING,
    AZURE_IOT_HUB_DEVICE_ID,
)

logger = logging.getLogger(__name__)


class AzureIoTClient:
    """Client for communicating with Azure IoT Hub."""

    def __init__(self, connection_string: Optional[str] = None, device_id: Optional[str] = None):
        """
        Initialize Azure IoT Hub client.

        Args:
            connection_string: IoT Hub connection string (uses env var if not provided)
            device_id: Device identifier (uses env var if not provided)
        """
        self.connection_string = connection_string or AZURE_IOT_HUB_CONNECTION_STRING
        self.device_id = device_id or AZURE_IOT_HUB_DEVICE_ID
        self._client = None
        self._connected = False

    def connect(self) -> bool:
        """
        Establish connection to Azure IoT Hub.

        Returns:
            True if connection successful, False otherwise
        """
        if not self.connection_string:
            logger.warning("No Azure IoT Hub connection string configured")
            return False

        try:
            from azure.iot.device import IoTHubDeviceClient

            self._client = IoTHubDeviceClient.create_from_connection_string(
                self.connection_string
            )
            self._client.connect()
            self._connected = True
            logger.info(f"Connected to Azure IoT Hub as device: {self.device_id}")
            return True
        except ImportError:
            logger.error("azure-iot-device not installed. Use: pip install azure-iot-device")
            return False
        except Exception as e:
            logger.error(f"Failed to connect to Azure IoT Hub: {e}")
            return False

    def disconnect(self) -> None:
        """Disconnect from Azure IoT Hub."""
        if self._client and self._connected:
            try:
                self._client.shutdown()
                self._connected = False
                logger.info("Disconnected from Azure IoT Hub")
            except Exception as e:
                logger.error(f"Error disconnecting from Azure IoT Hub: {e}")

    def send_telemetry(self, data: dict[str, Any]) -> bool:
        """
        Send telemetry data to Azure IoT Hub.

        Args:
            data: Telemetry data dictionary

        Returns:
            True if send successful, False otherwise
        """
        if not self._connected or not self._client:
            logger.warning("Not connected to Azure IoT Hub")
            return False

        try:
            from azure.iot.device import Message

            # Add metadata
            telemetry = {
                "device_id": self.device_id,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "data": data,
            }

            message = Message(json.dumps(telemetry))
            message.content_encoding = "utf-8"
            message.content_type = "application/json"

            self._client.send_message(message)
            logger.debug(f"Telemetry sent: {telemetry}")
            return True
        except Exception as e:
            logger.error(f"Failed to send telemetry: {e}")
            return False

    def receive_message(self, timeout: int = 10) -> Optional[dict[str, Any]]:
        """
        Receive a message from Azure IoT Hub (direct methods, twin updates).

        Args:
            timeout: Timeout in seconds

        Returns:
            Received message data or None
        """
        if not self._connected or not self._client:
            return None

        try:
            # This is a simplified implementation
            # In production, use callbacks or async patterns
            logger.debug("Waiting for messages...")
            return None
        except Exception as e:
            logger.error(f"Error receiving message: {e}")
            return None

    @property
    def is_connected(self) -> bool:
        """Check if client is connected."""
        return self._connected


class LocalFileClient:
    """Fallback client for local file-based data exchange."""

    def __init__(self, data_dir: str = "monitor"):
        """
        Initialize local file client.

        Args:
            data_dir: Directory to store data files
        """
        import os

        self.data_dir = data_dir
        self.latest_file = os.path.join(data_dir, "latest_reading.json")
        self.history_dir = os.path.join(data_dir, "history")
        os.makedirs(self.history_dir, exist_ok=True)
        logger.info(f"Local file client initialized: {self.data_dir}")

    def send_telemetry(self, data: dict[str, Any]) -> bool:
        """
        Save telemetry data to local files.

        Args:
            data: Telemetry data dictionary

        Returns:
            True if save successful
        """
        try:
            import os

            # Save latest reading
            with open(self.latest_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            # Append to history
            timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
            history_file = os.path.join(self.history_dir, f"reading_{timestamp}.json")
            with open(history_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            logger.debug(f"Data saved to {self.latest_file}")
            return True
        except Exception as e:
            logger.error(f"Failed to save data: {e}")
            return False

    def read_latest(self) -> Optional[dict[str, Any]]:
        """
        Read the latest reading from file.

        Returns:
            Latest reading data or None
        """
        try:
            import os

            if os.path.exists(self.latest_file):
                with open(self.latest_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            return None
        except Exception as e:
            logger.error(f"Failed to read latest data: {e}")
            return None

    def read_history(self, limit: int = 100) -> list[dict[str, Any]]:
        """
        Read historical data.

        Args:
            limit: Maximum number of readings to return

        Returns:
            List of historical readings
        """
        try:
            import os

            readings = []
            files = sorted(
                [f for f in os.listdir(self.history_dir) if f.endswith(".json")],
                reverse=True,
            )[:limit]

            for filename in files:
                filepath = os.path.join(self.history_dir, filename)
                with open(filepath, "r", encoding="utf-8") as f:
                    readings.append(json.load(f))

            return readings
        except Exception as e:
            logger.error(f"Failed to read history: {e}")
            return []


def create_azure_client(
    use_azure: bool = False,
    connection_string: Optional[str] = None,
    device_id: Optional[str] = None,
    data_dir: str = "monitor",
) -> Any:
    """
    Factory function to create appropriate client.

    Args:
        use_azure: Whether to use Azure IoT Hub or local files
        connection_string: Azure IoT Hub connection string
        device_id: Device identifier
        data_dir: Local data directory (for file client)

    Returns:
        AzureIoTClient or LocalFileClient instance
    """
    if use_azure and connection_string:
        client = AzureIoTClient(connection_string=connection_string, device_id=device_id)
        if client.connect():
            return client
        logger.warning("Falling back to local file client")

    return LocalFileClient(data_dir=data_dir)
