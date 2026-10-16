"""Report which expected sensor addresses appear on Raspberry Pi I2C bus 1."""

import subprocess


EXPECTED_SENSORS = (
    ("SHT45", (0x44,)),
    ("ADXL345", (0x53, 0x1D)),
    ("BME690", (0x76, 0x77)),
    ("VL53L8CX", (0x29,)),
)


def addresses_from_i2cdetect(output):
    found = set()

    for line in output.splitlines():
        if ":" not in line:
            continue

        row, cells = line.split(":", 1)
        if len(row.strip()) != 2:
            continue

        for cell in cells.split():
            if len(cell) == 2 and all(character in "0123456789abcdefABCDEF" for character in cell):
                found.add(int(cell, 16))

    return found


def report(found):
    print("I2C bus 1 responding addresses: {}".format(
        ", ".join("0x{:02X}".format(address) for address in sorted(found)) or "none"
    ))

    for sensor_name, candidate_addresses in EXPECTED_SENSORS:
        matching = [address for address in candidate_addresses if address in found]
        if matching:
            addresses = ", ".join("0x{:02X}".format(address) for address in matching)
            print("FOUND   {} at {}".format(sensor_name, addresses))
        else:
            expected = " / ".join("0x{:02X}".format(address) for address in candidate_addresses)
            print("MISSING {} (expected {})".format(sensor_name, expected))


def main():
    try:
        result = subprocess.run(
            ["i2cdetect", "-y", "1"],
            check=True,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError:
        raise SystemExit("i2cdetect is missing. Install it with: sudo apt install i2c-tools")
    except subprocess.CalledProcessError as error:
        details = (error.stderr or error.stdout or str(error)).strip()
        raise SystemExit("I2C scan failed: {}".format(details))

    report(addresses_from_i2cdetect(result.stdout))


if __name__ == "__main__":
    main()
