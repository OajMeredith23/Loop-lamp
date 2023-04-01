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

wifi.radio.connect(os.getenv('CIRCUITPY_WIFI_SSID'), os.getenv('CIRCUITPY_WIFI_PASSWORD'))

# Use cityname, country code where countrycode is ISO3166 format.
# E.g. "New York, US" or "London, GB"
location = "London, UK"

# openweathermap URL, brings in your location & your token
url = "http://api.openweathermap.org/data/2.5/weather?q="+location
url += "&appid="+os.getenv('openweather_token')

print(url)
pool = socketpool.SocketPool(wifi.radio)
requests = adafruit_requests.Session(pool, ssl.create_default_context())

def get_timezone(fetch_weather):
    #  pings openweather
    if(fetch_weather):
        response = requests.get(url)
        #  packs the response into a JSON
        response_as_json = response.json()
        timezone = response_as_json["timezone"]
        
        if(timezone == "3600"):
            timezone = 'BST'
        else:
            timezone = 'GMT'
        #  delay for 5 minutes
    return timezone


