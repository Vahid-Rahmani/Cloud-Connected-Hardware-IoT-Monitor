# Pico 2 W sensor bring-up

The first firmware milestone checks whether the four sensor breakouts acknowledge on I²C. It intentionally does not initialize drivers or claim that measurements work yet.

## Bus wiring

| Pico 2 W | Connects to |
| --- | --- |
| GP2 | SDA on all four breakouts |
| GP3 | SCL on all four breakouts |
| GND | GND on all four breakouts |
| 3V3 or a breakout's documented supply input | Sensor power, only when supported by that breakout |

Use the voltage and pin documentation for each exact breakout. Keep signals connected to Pico GPIO within its 3.3 V logic range. If a breakout exposes LPn, reset, or interrupt pins, follow that board's own startup requirements.

## Run

1. Install MicroPython for Pico 2 W.
2. Copy this folder's `main.py` to the board as `main.py`.
3. Open the serial REPL and check the scan output.

The starter uses I²C controller 1 at 100 kHz on GP2/GP3. Change these constants only after checking the physical wiring.

Expected 7-bit addresses: SHT45 `0x44`; ADXL345 `0x53` or `0x1D`; BME690 `0x76` or `0x77`; VL53L8CX `0x29`.
