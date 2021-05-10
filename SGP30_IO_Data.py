#SPDX-FileCopyrightText: 2021 Rodrigo Argumedo for Adafruit Industries
#SPDX-License-Identifier: MIT

""" Example for using the SGP30 with CircuitPython and the Adafruit library"""

import ssl
import time
import board
import busio
import adafruit_requests
import socketpool
import wifi
from adafruit_io.adafruit_io import IO_HTTP, AdafruitIO_RequestError
import adafruit_sgp30

try:
	from secrets import secrets
except ImportError:
	print("WiFi secrets are kept in secrets.py, please add them there!")
	raise

i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)

# Create library object on our I2C port
sgp30 = adafruit_sgp30.Adafruit_SGP30(i2c)

print("SGP30 serial #", [hex(i) for i in sgp30.serial])

sgp30.iaq_init()
#sgp30.set_iaq_baseline(0x97f2, 0x9964)

elapsed_sec = 0

io_username = secrets['aio_username']
io_key = secrets['aio_key']

wifi.radio.connect(secrets["ssid"], secrets["password"])

pool = socketpool.SocketPool(wifi.radio)
requests = adafruit_requests.Session(pool, ssl.create_default_context())
io = IO_HTTP(io_username, io_key, requests)

try:
	while True:
		eCO2 = sgp30.eCO2
		TVOC = sgp30.TVOC
		print("eCO2 = %d ppm \t TVOC = %d ppb" % (eCO2, TVOC))
		time.sleep(1)
		elapsed_sec += 1
		if elapsed_sec > 10:
			base_eCO2 = sgp30.baseline_eCO2
			base_TVOC = sgp30.baseline_TVOC
			io.send_data("eco2-data", eCO2)
			io.send_data("tvoc-data", TVOC)
			elapsed_sec = 0
			print(
				"**** Baseline values: eCO2 = 0x%x, TVOC = 0x%x"
				% (base_eCO2, base_TVOC)
			)
except AdafruitIO_RequestError:
	print("Something went wrong. Please debug.")
	raise