# Cloud-Connected Hardware Monitor

A hardware-first monitoring project based on a **Raspberry Pi Pico 2 W** and four sensors:

| Component | What it measures |
| --- | --- |
| Sensirion SHT45 | Temperature and relative humidity |
| ADXL345 (GY-291 breakout) | Acceleration, movement, and vibration |
| Bosch BME690 | Temperature, humidity, pressure, and gas response |
| ST VL53L8CX | 8×8 multizone time-of-flight distance |

## Current status

The first milestone is **hardware bring-up**. The firmware in `hardware/pico2w/main.py` scans the shared I²C bus and reports which expected sensor addresses respond. It does not yet read measurements or send data over Wi-Fi.

The repository previously had a Windows Active Directory monitor in its root. That code is preserved under `legacy/windows-ad-monitor/`; it is not the Pico firmware or the hardware data collector.

## Bring-up

1. Install the MicroPython firmware for Raspberry Pi Pico 2 W using the [Raspberry Pi MicroPython guide](https://www.raspberrypi.com/documentation/microcontrollers/micropython.html).
2. Connect the sensors to one I²C bus. The starter uses GP2 for SDA and GP3 for SCL.
3. Check the voltage requirements and pin labels on each breakout board. Pico GPIO is 3.3 V logic; do not connect a 5 V signal to a Pico GPIO pin.
4. Copy `hardware/pico2w/main.py` to the Pico as `main.py`, then run it from Thonny or the MicroPython REPL.
5. Confirm that the four expected devices appear before adding sensor drivers.

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
