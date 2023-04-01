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


url = "http://worldtimeapi.org/api/timezone/Europe/"+os.getenv('location')

pool = socketpool.SocketPool(wifi.radio)
requests = adafruit_requests.Session(pool, ssl.create_default_context())

def get_time():
    #  pings openweather
    response = requests.get(url)
    #  packs the response into a JSON
    response_as_json = response.json()
   
    print(response_as_json)
    #splits [year, month, dayandtime]
    datetime_date_split = response_as_json["datetime"].split('-')
    year = datetime_date_split[0]
    month = datetime_date_split[1]
    
    datetime_day_time_split = datetime_date_split[2].split('T')
    day = datetime_day_time_split[0]
    
    datetime_time_split = datetime_day_time_split[1].split('.')[0].split(':')
    hour = datetime_time_split[0]
    min = datetime_time_split[1]
    sec = datetime_time_split[2]
    return (int(year), int(month), int(day), int(hour), int(min), int(sec), response_as_json["day_of_week"])