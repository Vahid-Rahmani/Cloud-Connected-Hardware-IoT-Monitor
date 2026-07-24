"""Validation utilities for IoT temperature monitoring data."""

import logging
from datetime import datetime, timezone
from typing import Any, Optional

from monitor.config import MONITOR_SCHEMA, TEMPERATURE_MAX, TEMPERATURE_MIN

logger = logging.getLogger(__name__)


class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass


def validate_temperature(temperature: Any) -> float:
    """
    Validate temperature value.

    Args:
        temperature: Temperature value to validate

    Returns:
        Validated temperature as float

    Raises:
        ValidationError: If temperature is invalid
    """
    if temperature is None:
        raise ValidationError("Temperature cannot be None")

    try:
        temp_float = float(temperature)
    except (TypeError, ValueError):
        raise ValidationError(f"Temperature must be a number, got: {type(temperature)}")

    if temp_float < TEMPERATURE_MIN or temp_float > TEMPERATURE_MAX:
        raise ValidationError(
            f"Temperature {temp_float}°C out of range [{TEMPERATURE_MIN}, {TEMPERATURE_MAX}]"
        )

    return temp_float


def validate_humidity(humidity: Any) -> Optional[float]:
    """
    Validate humidity value.

    Args:
        humidity: Humidity value to validate

    Returns:
        Validated humidity as float or None if not provided

    Raises:
        ValidationError: If humidity is invalid
    """
    if humidity is None:
        return None

    try:
        hum_float = float(humidity)
    except (TypeError, ValueError):
        raise ValidationError(f"Humidity must be a number, got: {type(humidity)}")

    if hum_float < 0 or hum_float > 100:
        raise ValidationError(f"Humidity {hum_float}% out of range [0, 100]")

    return hum_float


def validate_timestamp(timestamp: Any) -> str:
    """
    Validate and normalize timestamp.

    Args:
        timestamp: Timestamp to validate (ISO string or datetime)

    Returns:
        ISO-format timestamp string

    Raises:
        ValidationError: If timestamp is invalid
    """
    if timestamp is None:
        return datetime.now(timezone.utc).isoformat()

    if isinstance(timestamp, datetime):
        return timestamp.isoformat()

    if isinstance(timestamp, str):
        try:
            # Try parsing ISO format
            dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
            return dt.isoformat()
        except ValueError:
            raise ValidationError(f"Invalid timestamp format: {timestamp}")

    raise ValidationError(f"Timestamp must be string or datetime, got: {type(timestamp)}")


def validate_device_id(device_id: Any) -> str:
    """
    Validate device ID.

    Args:
        device_id: Device ID to validate

    Returns:
        Validated device ID string

    Raises:
        ValidationError: If device ID is invalid
    """
    if not device_id:
        raise ValidationError("Device ID cannot be empty")

    device_str = str(device_id).strip()

    if len(device_str) < 1 or len(device_str) > 128:
        raise ValidationError(f"Device ID length must be 1-128 characters, got: {len(device_str)}")

    return device_str


def validate_location(location: Any) -> dict[str, str]:
    """
    Validate location information.

    Args:
        location: Location dictionary to validate

    Returns:
        Validated location dictionary

    Raises:
        ValidationError: If location is invalid
    """
    if not isinstance(location, dict):
        raise ValidationError(f"Location must be a dictionary, got: {type(location)}")

    if "room" not in location or not location["room"]:
        raise ValidationError("Location must include 'room' field")

    validated = {"room": str(location["room"]).strip()}

    if "rack_id" in location and location["rack_id"]:
        validated["rack_id"] = str(location["rack_id"]).strip()

    if "zone" in location and location["zone"]:
        validated["zone"] = str(location["zone"]).strip()

    return validated


def validate_reading(data: dict[str, Any]) -> dict[str, Any]:
    """
    Validate a complete sensor reading.

    Args:
        data: Sensor reading dictionary

    Returns:
        Validated and normalized reading

    Raises:
        ValidationError: If reading is invalid
    """
    if not isinstance(data, dict):
        raise ValidationError(f"Reading must be a dictionary, got: {type(data)}")

    validated = {}

    # Validate device_id
    validated["device_id"] = validate_device_id(data.get("device_id"))

    # Validate timestamp
    validated["timestamp"] = validate_timestamp(data.get("timestamp"))

    # Validate temperature (required)
    validated["temperature"] = validate_temperature(data.get("temperature"))

    # Validate optional fields
    humidity = validate_humidity(data.get("humidity"))
    if humidity is not None:
        validated["humidity"] = humidity

    if "pressure" in data and data["pressure"] is not None:
        try:
            validated["pressure"] = float(data["pressure"])
        except (TypeError, ValueError):
            logger.warning(f"Invalid pressure value ignored: {data['pressure']}")

    # Validate location (required)
    validated["location"] = validate_location(data.get("location"))

    # Validate device_info (optional)
    if "device_info" in data and isinstance(data["device_info"], dict):
        validated["device_info"] = data["device_info"]

    # Validate status
    validated["status"] = data.get("status", "ok")

    return validated


def validate_schema_compliance(data: dict[str, Any]) -> bool:
    """
    Check if data conforms to the monitoring schema.

    Args:
        data: Data to validate

    Returns:
        True if compliant, False otherwise
    """
    try:
        # Basic schema validation (without jsonschema library)
        required_fields = MONITOR_SCHEMA.get("required", [])

        for field in required_fields:
            if field not in data:
                logger.warning(f"Missing required field: {field}")
                return False

        return True
    except Exception as e:
        logger.error(f"Schema validation error: {e}")
        return False
