"""I2C bring-up scan for Raspberry Pi Pico 2 W.

This is a bus-discovery milestone only; it does not yet read sensor values.
"""

from machine import I2C, Pin
from time import sleep


I2C_ID = 1
SDA_PIN = 2
SCL_PIN = 3
I2C_FREQUENCY_HZ = 100_000
SCAN_INTERVAL_SECONDS = 5

EXPECTED_SENSORS = (
    ("SHT45", (0x44,)),
    ("ADXL345", (0x53, 0x1D)),
    ("BME690", (0x76, 0x77)),
    ("VL53L8CX", (0x29,)),
)


def report_scan(i2c):
    found = set(i2c.scan())
    printable = ", ".join("0x{:02X}".format(address) for address in sorted(found))
    print("I2C{} scan on GP{} / GP{}: [{}]".format(I2C_ID, SDA_PIN, SCL_PIN, printable))

    for sensor_name, candidate_addresses in EXPECTED_SENSORS:
        matching = [address for address in candidate_addresses if address in found]
        if matching:
            addresses = ", ".join("0x{:02X}".format(address) for address in matching)
            print("  FOUND  {} at {}".format(sensor_name, addresses))
        else:
            expected = " / ".join("0x{:02X}".format(address) for address in candidate_addresses)
            print("  MISSING {} (expected {})".format(sensor_name, expected))

    known_addresses = {
        address
        for _, candidate_addresses in EXPECTED_SENSORS
        for address in candidate_addresses
    }
    for address in sorted(found - known_addresses):
        print("  OTHER  device at 0x{:02X}".format(address))


def main():
    i2c = I2C(
        I2C_ID,
        sda=Pin(SDA_PIN),
        scl=Pin(SCL_PIN),
        freq=I2C_FREQUENCY_HZ,
    )

    print("Pico 2 W sensor bus bring-up")
    print("No sensor measurements are read in this milestone.")

    while True:
        try:
            report_scan(i2c)
        except OSError as error:
            print("I2C scan failed: {}".format(error))
        sleep(SCAN_INTERVAL_SECONDS)


if __name__ == "__main__":
    main()
