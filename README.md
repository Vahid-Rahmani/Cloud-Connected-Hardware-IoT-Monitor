# Cloud-Connected Hardware Monitor

A hardware-first monitoring project for a **Raspberry Pi 2 Model B Rev 1.1** and four sensors:

| Component | What it measures |
| --- | --- |
| Sensirion SHT45 | Temperature and relative humidity |
| ADXL345 (GY-291 breakout) | Acceleration, movement, and vibration |
| Bosch BME690 | Temperature, humidity, pressure, and gas response |
| ST VL53L8CX | 8×8 multizone time-of-flight distance |

## Current status

The project runs on Raspberry Pi OS and uses normal Python 3. The first milestone is **I²C bus bring-up**: `hardware/raspberry-pi-2/scan_i2c.py` checks which expected sensor addresses respond. It does not yet read measurements or send data over Wi-Fi.

The previous Windows Active Directory prototype is preserved under `legacy/windows-ad-monitor/` and is not part of the hardware data path.

Raspberry Pi 2 uses a 32-bit processor family; Raspberry Pi OS provides a 32-bit image for Raspberry Pi 2. Use the OS already installed on the board for the first test, and check its release before adding sensor libraries.

## Bring-up

1. Enable I²C in Raspberry Pi OS.
2. Connect the sensor breakouts to GPIO2/SDA1, GPIO3/SCL1, and common GND. Check the voltage rating of each breakout before powering it.
3. Install `i2c-tools`.
4. Run `sudo python3 hardware/raspberry-pi-2/scan_i2c.py`.
5. Confirm all four devices appear before installing or writing sensor drivers.

Expected default 7-bit addresses:

| Sensor | Address |
| --- | --- |
| SHT45 | `0x44` |
| ADXL345 | `0x53` or `0x1D` |
| BME690 | `0x76` or `0x77` |
| VL53L8CX | `0x29` |

Breakout configuration can change an address or require an enable/reset pin. Use the documentation for the exact boards that were purchased.

## Next milestones

- Read and validate measurements from each sensor.
- Define a small, versioned telemetry message.
- Add Wi-Fi transport and an authenticated receiver.
- Add local history and a dashboard, then cloud forwarding.

Keep sensor readings as the source of truth. Add alerting and AI explanations only after the measurement path is reliable.
