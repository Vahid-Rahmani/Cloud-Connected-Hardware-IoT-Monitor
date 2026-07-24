"""Sensor module for reading temperature data from hardware sensors."""

import logging
import time
from datetime import datetime, timezone
from typing import Any, Optional

logger = logging.getLogger(__name__)


class TemperatureSensor:
    """Base class for temperature sensors."""

    def __init__(self, sensor_type: str, gpio_pin: int = 4):
        """
        Initialize the temperature sensor.

        Args:
            sensor_type: Type of sensor (dht22, sht31, ds18b20, bme280)
            gpio_pin: GPIO pin number for the sensor data line
        """
        self.sensor_type = sensor_type.lower()
        self.gpio_pin = gpio_pin
        self._sensor = None
        self._initialize_sensor()

    def _initialize_sensor(self) -> None:
        """Initialize the sensor based on type."""
        try:
            if self.sensor_type == "dht22":
                self._init_dht22()
            elif self.sensor_type == "sht31":
                self._init_sht31()
            elif self.sensor_type == "ds18b20":
                self._init_ds18b20()
            elif self.sensor_type == "bme280":
                self._init_bme280()
            else:
                raise ValueError(f"Unsupported sensor type: {self.sensor_type}")
        except Exception as e:
            logger.error(f"Failed to initialize {self.sensor_type} sensor: {e}")
            self._sensor = None

    def _init_dht22(self) -> None:
        """Initialize DHT22 sensor."""
        try:
            import board
            import adafruit_dht

            self._sensor = adafruit_dht.DHT22(getattr(board, f"D{self.gpio_pin}"))
            logger.info(f"DHT22 sensor initialized on GPIO{self.gpio_pin}")
        except ImportError:
            logger.warning("adafruit_dht not installed. Use: pip install adafruit-circuitpython-dht")
            self._sensor = None

    def _init_sht31(self) -> None:
        """Initialize SHT31 sensor."""
        try:
            import board
            import adafruit_sht31d

            i2c = board.I2C()
            self._sensor = adafruit_sht31d.SHT31D(i2c)
            logger.info("SHT31 sensor initialized on I2C")
        except ImportError:
            logger.warning("adafruit_sht31d not installed. Use: pip install adafruit-circuitpython-sht31d")
            self._sensor = None

    def _init_ds18b20(self) -> None:
        """Initialize DS18B20 sensor (1-Wire protocol)."""
        try:
            import glob

            base_dir = "/sys/bus/w1/devices/"
            device_folders = glob.glob(base_dir + "28*")
            if device_folders:
                self._sensor = device_folders[0] + "/w1_slave"
                logger.info(f"DS18B20 sensor initialized: {device_folders[0]}")
            else:
                logger.warning("No DS18B20 sensor found. Check wiring and enable 1-Wire.")
                self._sensor = None
        except Exception as e:
            logger.error(f"DS18B20 initialization failed: {e}")
            self._sensor = None

    def _init_bme280(self) -> None:
        """Initialize BME280 sensor."""
        try:
            import board
            import adafruit_bme280

            i2c = board.I2C()
            self._sensor = adafruit_bme280.Adafruit_BME280_I2C(i2c, address=0x76)
            logger.info("BME280 sensor initialized on I2C")
        except ImportError:
            logger.warning("adafruit_bme280 not installed. Use: pip install adafruit-circuitpython-bme280")
            self._sensor = None

    def read(self) -> Optional[dict[str, Any]]:
        """
        Read temperature and optional humidity data from sensor.

        Returns:
            Dictionary with temperature and humidity data, or None on failure
        """
        if self._sensor is None:
            logger.warning("Sensor not initialized")
            return None

        try:
            if self.sensor_type == "dht22":
                return self._read_dht22()
            elif self.sensor_type == "sht31":
                return self._read_sht31()
            elif self.sensor_type == "ds18b20":
                return self._read_ds18b20()
            elif self.sensor_type == "bme280":
                return self._read_bme280()
        except Exception as e:
            logger.error(f"Error reading {self.sensor_type} sensor: {e}")
            return None

    def _read_dht22(self) -> Optional[dict[str, Any]]:
        """Read from DHT22 sensor."""
        try:
            temperature = self._sensor.temperature
            humidity = self._sensor.humidity
            if temperature is not None and humidity is not None:
                return {
                    "temperature": round(temperature, 2),
                    "humidity": round(humidity, 2),
                }
            return None
        except RuntimeError as e:
            logger.warning(f"DHT22 read error: {e}")
            return None

    def _read_sht31(self) -> Optional[dict[str, Any]]:
        """Read from SHT31 sensor."""
        try:
            temperature = self._sensor.temperature
            humidity = self._sensor.relative_humidity
            if temperature is not None and humidity is not None:
                return {
                    "temperature": round(temperature, 2),
                    "humidity": round(humidity, 2),
                }
            return None
        except Exception as e:
            logger.warning(f"SHT31 read error: {e}")
            return None

    def _read_ds18b20(self) -> Optional[dict[str, Any]]:
        """Read from DS18B20 sensor."""
        try:
            with open(self._sensor, "r") as f:
                lines = f.readlines()

            if lines[0].strip()[-3:] != "YES":
                logger.warning("DS18B20 CRC check failed")
                return None

            equals_pos = lines[1].find("t=")
            if equals_pos != -1:
                temp_string = lines[1][equals_pos + 2:]
                temperature = float(temp_string) / 1000.0
                return {"temperature": round(temperature, 2)}
            return None
        except Exception as e:
            logger.warning(f"DS18B20 read error: {e}")
            return None

    def _read_bme280(self) -> Optional[dict[str, Any]]:
        """Read from BME280 sensor."""
        try:
            temperature = self._sensor.temperature
            humidity = self._sensor.humidity
            pressure = self._sensor.pressure
            return {
                "temperature": round(temperature, 2),
                "humidity": round(humidity, 2),
                "pressure": round(pressure, 2),
            }
        except Exception as e:
            logger.warning(f"BME280 read error: {e}")
            return None

    def close(self) -> None:
        """Clean up sensor resources."""
        if self._sensor is not None and hasattr(self._sensor, "exit"):
            self._sensor.exit()
        logger.info(f"{self.sensor_type} sensor closed")


class SimulatedSensor:
    """Simulated sensor for testing without hardware."""

    def __init__(self, base_temp: float = 24.0, variation: float = 2.0):
        """
        Initialize simulated sensor.

        Args:
            base_temp: Base temperature in Celsius
            variation: Temperature variation range
        """
        self.base_temp = base_temp
        self.variation = variation
        self._last_temp = base_temp
        logger.info(f"Simulated sensor initialized (base: {base_temp}°C)")

    def read(self) -> dict[str, Any]:
        """
        Generate a simulated temperature reading.

        Returns:
            Dictionary with simulated temperature and humidity
        """
        import random

        # Simulate temperature variation
        delta = random.uniform(-self.variation, self.variation)
        self._last_temp = max(-10, min(50, self._last_temp + delta))

        # Simulate humidity (inverse correlation with temperature)
        base_humidity = 50.0
        humidity_delta = (self._last_temp - self.base_temp) * 2
        humidity = max(20, min(80, base_humidity - humidity_delta))

        return {
            "temperature": round(self._last_temp, 2),
            "humidity": round(humidity, 2),
        }

    def close(self) -> None:
        """No cleanup needed for simulated sensor."""
        pass


def create_sensor(
    sensor_type: str = "simulated",
    gpio_pin: int = 4,
    base_temp: float = 24.0,
) -> Any:
    """
    Factory function to create a sensor instance.

    Args:
        sensor_type: Type of sensor (dht22, sht31, ds18b20, bme280, simulated)
        gpio_pin: GPIO pin number (for hardware sensors)
        base_temp: Base temperature for simulated sensor

    Returns:
        Sensor instance (TemperatureSensor or SimulatedSensor)
    """
    if sensor_type.lower() == "simulated":
        return SimulatedSensor(base_temp=base_temp)
    else:
        return TemperatureSensor(sensor_type=sensor_type, gpio_pin=gpio_pin)
