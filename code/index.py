import busio
import adafruit_pcf8523
import time
import board
import digitalio
import os
import ipaddress
import wifi
import socketpool
import microcontroller
import adafruit_requests
import ssl

from tilt import getTiltPos
from chime import chime
from reading_light import reading_light
from weather import get_weather
from get_time import get_time

import neopixel


# Update this to match the number of NeoPixel LEDs connected to your board.
num_pixels = 26

pixels = neopixel.NeoPixel(board.GP6, num_pixels)
  
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

myI2C = busio.I2C(scl=board.GP1, sda=board.GP0)
rtc = adafruit_pcf8523.PCF8523(myI2C)
    
prev_min = 0
prev_hour = 0
pixels_color = (0,0,0)

print("Connecting to WiFi")

#  connect to your SSID
wifi.radio.connect(os.getenv('CIRCUITPY_WIFI_SSID'), os.getenv('CIRCUITPY_WIFI_PASSWORD'))

print("Connected to WiFi")
pool = socketpool.SocketPool(wifi.radio)
requests = adafruit_requests.Session(pool, ssl.create_default_context())


quotes_url = "https://www.adafruit.com/api/quotes.php"

current_time = get_time()

t = time.struct_time((current_time[0], current_time[1], current_time[2], current_time[3], current_time[4], current_time[5], current_time[6],   -1,    -1))
# you must set year, mon, date, hour, min, sec and weekday
# yearday is not supported, isdst can be set but we don't do anything with it at this time
print("Setting time to:", t)     # uncomment for debugging
rtc.datetime = t
    
CHIME_TIME = 15 #minutes
orientation = False
prev_orientation = False

while True:
    try:
        t = rtc.datetime
        #print("The date is %d/%d/%d" % (t.tm_mday, t.tm_mon, t.tm_year))
        #print("The time is %d:%02d:%02d" % (t.tm_hour, t.tm_min, t.tm_sec))

        # getTiltPos returns true if tilt sensor is active (i.e. loop lamp is vertical)
        orientation = getTiltPos()
    
        do_chime = t.tm_min % CHIME_TIME == 0
        
        if(orientation):
            chime_amount = 3
            if(prev_hour != t.tm_hour):
                chime_amount = t.tm_hour % 12
            #print("chime_amount", chime_amount)
            if(orientation != prev_orientation):
                print("Flipped")
                current_weather = get_weather()
                print("current_weather", current_weather)
                pixels_color = (255, 10, 160)
            chime(pixels, do_chime, chime_amount)
        else:
            pixels_color =  reading_light()
        
        pixels.fill(pixels_color)
        prev_min = t.tm_min
        prev_hour = t.tm_hour
        
        prev_orientation = orientation
    except Exception as e:
        print("Error:\n", str(e))
        print("Resetting microcontroller in 10 seconds")
        time.sleep(10)
        microcontroller.reset()
#time.sleep(1)
        
    
        
    