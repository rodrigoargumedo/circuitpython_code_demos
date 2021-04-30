import time
import board
import busio
import terminalio
from adafruit_magtag.magtag import MagTag
from adafruit_scd30 import SCD30
from adafruit_tsl2591 import TSL2591

try:
    from secrets import secrets
except ImportError:
    raise ImportError("Please add your Adafruit IO and WiFi secrets into secrets.py. Exiting.")

device = MagTag()

scd = SCD30(board.I2C())
tsl = TSL2591(board.I2C())

# We'll connect this MagTag to the internet if we need to use Adafruit IO connectivity.
# device.network.connect()

device.add_text(
    text_font=terminalio.FONT,
    text_position=(
        10,
        (device.graphics.display.height // 2) - 1,
    ),
    text_scale=1,
)

device.set_text("Select a mode:\na. CO2 and Temperature\nb. Humidity\nc.Infrared Light\nd.Visible Light\nWant to start over? Press Reset to go back.")

buttons = device.peripherals.buttons

while True:

    # When button A is pressed, then show CO2 and temperature
    if device.peripherals.button_a_pressed:
        co2 = scd.CO2
        temperature = scd.temperature
        print("Current CO2: {:.2f}".format(co2))
        print("Current Temperature: {:.2f}".format(temperature))
        device.set_text('Current CO2: {:.2f} ppm\nCurrent Temperature: {:.2f} C'.format(co2, temperature))

    # When button B is pressed, then show Humidity
    if device.peripherals.button_b_pressed:
        humidity = scd.relative_humidity
        print("Current Humidity: {:.2f}%rH".format(humidity))
        device.set_text("Current Humidity: {:.2f} %rH".format(humidity))

    # When button C is pressed, then show infrared light
    if device.peripherals.button_c_pressed:
         infrared = tsl.infrared
         print("Current infrared light: {:.2f}".format(infrared))
         device.set_text("Current infrared light: {:.2f} lux".format(infrared))

    # When button D is pressed, then show Visible Light
    if device.peripherals.button_d_pressed:
        visible = tsl.visible
        print("Current visible light: {:.2f} lux".format(visible))
        device.set_text("Current visible light: {:.2f} lux".format(visible))
