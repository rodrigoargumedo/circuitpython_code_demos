# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

""" Example for using the SGP30 with CircuitPython and the Adafruit library"""

import time
import board
import busio
import adafruit_sgp30
from adafruit_magtag import MagTag

magtag = MagTag.MagTag(rotation=180)

i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)

# Create library object on our I2C port
sgp30 = adafruit_sgp30.Adafruit_SGP30(i2c)

print("SGP30 serial #", [hex(i) for i in sgp30.serial])

sgp30.iaq_init()
#sgp30.set_iaq_baseline(0x8973, 0x8AAE)

magtag.refresh()
time.sleep(5)

elapsed_sec = 0

magtag.add_text(
    text_position=(
        (magtag.graphics.display.width // 2) - 1,
        (magtag.graphics.display.height // 2) - 1,
    ),
    text_scale=1.5,
    text_anchor_point=(0.5, 0.5)
)

show_display = True
internet_enabled = True

def measure_eco2(value):
    if value >= 400 and value <= 1000:
        return "Excellent"
    if value > 1000 and value <= 2000:
        return "Fair"
    if value > 2000 and value <= 5000:
        return "Poor"
    if value > 5000:
        return "Bad"

try:
    while True:
        if show_display:
            b_eCO2 = sgp30.baseline_eCO2
            b_TVOC = sgp30.baseline_TVOC
            eCO2 = sgp30.eCO2
            TVOC = sgp30.TVOC
            print("eCO2 = %d ppm \t TVOC = %d ppb" % (eCO2, TVOC))
            magtag.set_text("eCO2: %d\nppm\n\n%s\n\nTVOC: %d\nppb" % (eCO2,measure_eco2(eCO2), TVOC))
            time.sleep(60)
            elapsed_sec += 60
            if internet_enabled:
                magtag.push_to_io("eco2-data", eCO2)
                magtag.push_to_io("tvoc-data", TVOC)
                if elapsed_sec >= 120:
                    elapsed_sec = 0
                    print(
                        "**** Baseline values: eCO2 = 0x%x, TVOC = 0x%x"
                        % (b_eCO2, b_TVOC)
                    )
            if elapsed_sec >= 120:
                    elapsed_sec = 0
                    print(
                        "**** Baseline values: eCO2 = 0x%x, TVOC = 0x%x"
                        % (sgp30.baseline_eCO2, sgp30.baseline_TVOC)
                    )
    print("Display is disabled. Please modify code.py to enable it.")
    magtag.exit_and_deep_sleep(90)
except (ValueError, RuntimeError, OSError) as e:
    print("Something went wrong. See stack trace below.", e)
    magtag.exit_and_deep_sleep(30)