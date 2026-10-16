# Raspberry Pi 2 Model B sensor bring-up

This board runs Linux and uses ordinary Python 3. Enable the Linux I²C interface before using the sensors.

## Enable I²C

From the desktop, open Preferences → Control Centre → Interfaces and enable I²C.

Or run:

```bash
sudo raspi-config
```

Choose Interface Options → I2C → Enable, then reboot.

Install the scanner utility:

```bash
sudo apt update
sudo apt install -y i2c-tools
```

## Check the bus

Connect the four breakout boards to the Pi's I²C bus:

| Raspberry Pi 2 Model B | Sensor boards |
| --- | --- |
| Physical pin 3 / GPIO2 / SDA1 | SDA |
| Physical pin 5 / GPIO3 / SCL1 | SCL |
| GND | GND |
| 3.3 V or each breakout's documented supply input | Power, only as supported by that breakout |

The Pi's GPIO signals are 3.3 V. Confirm the voltage rating of every breakout and do not apply 5 V to GPIO2 or GPIO3.

Run:

```bash
sudo python3 hardware/raspberry-pi-2/scan_i2c.py
```

The scanner calls `i2cdetect -y 1` and reports the expected sensor addresses:

- SHT45: `0x44`
- ADXL345: `0x53` or `0x1D`
- BME690: `0x76` or `0x77`
- VL53L8CX: `0x29`

This verifies bus visibility only. Sensor drivers and measurement reads come in the next milestone. Use the exact breakout-board documentation if a device is absent; some breakouts need a separate enable/reset pin or use a different address setting.
