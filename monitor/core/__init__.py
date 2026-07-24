"""Core module for IoT temperature monitoring."""

from monitor.core.alerts import AlertManager
from monitor.core.azure_client import AzureIoTClient, LocalFileClient, create_azure_client
from monitor.core.sensor import SimulatedSensor, TemperatureSensor, create_sensor

__all__ = [
    "AlertManager",
    "AzureIoTClient",
    "LocalFileClient",
    "TemperatureSensor",
    "SimulatedSensor",
    "create_azure_client",
    "create_sensor",
]
