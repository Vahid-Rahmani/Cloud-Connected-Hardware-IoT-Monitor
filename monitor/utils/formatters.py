"""Formatting utilities for IoT temperature monitoring data."""

import logging
from datetime import datetime, timezone
from typing import Any, Optional

logger = logging.getLogger(__name__)


def format_temperature(temp: float, unit: str = "C", precision: int = 1) -> str:
    """
    Format temperature value for display.

    Args:
        temp: Temperature value
        unit: Temperature unit (C, F, K)
        precision: Decimal places

    Returns:
        Formatted temperature string
    """
    if unit.upper() == "F":
        temp = temp * 9 / 5 + 32
        symbol = "°F"
    elif unit.upper() == "K":
        temp = temp + 273.15
        symbol = "K"
    else:
        symbol = "°C"

    return f"{temp:.{precision}f}{symbol}"


def format_humidity(humidity: Optional[float], precision: int = 1) -> str:
    """
    Format humidity value for display.

    Args:
        humidity: Humidity percentage
        precision: Decimal places

    Returns:
        Formatted humidity string
    """
    if humidity is None:
        return "N/A"
    return f"{humidity:.{precision}f}%"


def format_pressure(pressure: Optional[float], precision: int = 1) -> str:
    """
    Format pressure value for display.

    Args:
        pressure: Pressure in hPa
        precision: Decimal places

    Returns:
        Formatted pressure string
    """
    if pressure is None:
        return "N/A"
    return f"{pressure:.{precision}f} hPa"


def format_timestamp(
    timestamp: Any,
    format_str: str = "%Y-%m-%d %H:%M:%S",
    include_tz: bool = False,
) -> str:
    """
    Format timestamp for display.

    Args:
        timestamp: Timestamp (string, datetime, or epoch)
        format_str: strftime format string
        include_tz: Include timezone info

    Returns:
        Formatted timestamp string
    """
    if timestamp is None:
        return "Never"

    if isinstance(timestamp, str):
        try:
            dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        except ValueError:
            return timestamp
    elif isinstance(timestamp, datetime):
        dt = timestamp
    elif isinstance(timestamp, (int, float)):
        dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
    else:
        return str(timestamp)

    formatted = dt.strftime(format_str)

    if include_tz and dt.tzinfo:
        formatted += " UTC"

    return formatted


def format_duration(seconds: float) -> str:
    """
    Format duration in human-readable format.

    Args:
        seconds: Duration in seconds

    Returns:
        Formatted duration string
    """
    if seconds < 60:
        return f"{seconds:.0f}s"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f}m"
    elif seconds < 86400:
        hours = seconds / 3600
        return f"{hours:.1f}h"
    else:
        days = seconds / 86400
        return f"{days:.1f}d"


def format_status_emoji(status: str) -> str:
    """
    Format status with emoji indicator.

    Args:
        status: Status string (ok, warning, critical, error)

    Returns:
        Status with emoji
    """
    emojis = {
        "ok": "🟢",
        "warning": "🟠",
        "critical": "🔴",
        "error": "❌",
    }
    emoji = emojis.get(status.lower(), "⚪")
    return f"{emoji} {status.upper()}"


def format_device_info(device_info: dict[str, Any]) -> str:
    """
    Format device information for display.

    Args:
        device_info: Device information dictionary

    Returns:
        Formatted device info string
    """
    parts = []

    if "type" in device_info:
        parts.append(device_info["type"].upper())

    if "sensor_type" in device_info:
        parts.append(device_info["sensor_type"].upper())

    if "firmware_version" in device_info:
        parts.append(f"v{device_info['firmware_version']}")

    return " | ".join(parts) if parts else "Unknown Device"


def format_location(location: dict[str, str]) -> str:
    """
    Format location for display.

    Args:
        location: Location dictionary

    Returns:
        Formatted location string
    """
    parts = [location.get("room", "Unknown Room")]

    if "rack_id" in location:
        parts.append(f"Rack {location['rack_id']}")

    if "zone" in location:
        parts.append(f"Zone {location['zone']}")

    return " - ".join(parts)


def format_reading_summary(reading: dict[str, Any]) -> str:
    """
    Format a complete reading for summary display.

    Args:
        reading: Sensor reading dictionary

    Returns:
        Formatted reading summary
    """
    temp = reading.get("temperature", 0)
    humidity = reading.get("humidity")
    location = reading.get("location", {})
    status = reading.get("status", "ok")

    summary = f"{format_status_emoji(status)} "
    summary += f"{format_temperature(temp)} "

    if humidity is not None:
        summary += f"/ {format_humidity(humidity)} "

    summary += f"- {format_location(location)}"

    return summary


def celsius_to_fahrenheit(celsius: float) -> float:
    """
    Convert Celsius to Fahrenheit.

    Args:
        celsius: Temperature in Celsius

    Returns:
        Temperature in Fahrenheit
    """
    return celsius * 9 / 5 + 32


def fahrenheit_to_celsius(fahrenheit: float) -> float:
    """
    Convert Fahrenheit to Celsius.

    Args:
        fahrenheit: Temperature in Fahrenheit

    Returns:
        Temperature in Celsius
    """
    return (fahrenheit - 32) * 5 / 9


def get_temperature_color(temp: float) -> str:
    """
    Get color based on temperature value.

    Args:
        temp: Temperature in Celsius

    Returns:
        Color name
    """
    if temp < 18:
        return "blue"
    elif temp < 24:
        return "green"
    elif temp < 28:
        return "orange"
    elif temp < 35:
        return "red"
    else:
        return "darkred"
