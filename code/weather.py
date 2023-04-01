# SPDX-FileCopyrightText: 2022 Liz Clark for Adafruit Industries
#
# SPDX-License-Identifier: MIT

import time
import os
import ssl
import wifi
import socketpool
import microcontroller
import adafruit_requests

#wifi.radio.connect(os.getenv('CIRCUITPY_WIFI_SSID'), os.getenv('CIRCUITPY_WIFI_PASSWORD'))

# Use cityname, country code where countrycode is ISO3166 format.
# E.g. "New York, US" or "London, GB"
#location = "London, UK"

# openweathermap URL, brings in your location & your token
url = "http://api.openweathermap.org/data/2.5/weather?q="+os.getenv('location')
url += "&appid="+os.getenv('openweather_token')

print(url)
pool = socketpool.SocketPool(wifi.radio)
requests = adafruit_requests.Session(pool, ssl.create_default_context())

def get_weather():
    #  pings openweather
    
    response = requests.get(url)
    #  packs the response into a JSON
    response_as_json = response.json()
    #  gets location name
    place = response_as_json['name']
    #  gets weather type (clouds, sun, etc)
    weather = response_as_json['weather'][0]['main']
    #  gets humidity %
    humidity = response_as_json['main']['humidity']
    #  gets air pressure in hPa
    pressure = response_as_json['main']['pressure']
    #  gets temp in kelvin
    temperature = response_as_json['main']['temp']
    #  converts temp from kelvin to F
    converted_temp = (temperature - 273.15) * 9/5 + 32
    #  converts temp from kelvin to C
    #  converted_temp = temperature - 273.15

    #  delay for 5 minutes
    return response_as_json['weather'][0]['main']

