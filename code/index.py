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
from weather_light_effects import weather_effect
import utils
import neopixel


# Update this to match the number of NeoPixel LEDs connected to your board.
num_pixels = os.getenv('num_pixels')

pixels = neopixel.NeoPixel(board.GP6, num_pixels)
  
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

myI2C = busio.I2C(scl=board.GP1, sda=board.GP0)
rtc = adafruit_pcf8523.PCF8523(myI2C)
    
prev_sec = 0
prev_min = 0
prev_hour = 0
pixels_color = (0,0,0)

print("Connecting to WiFi")

#  connect to your SSID
wifi.radio.connect(os.getenv('CIRCUITPY_WIFI_SSID'), os.getenv('CIRCUITPY_WIFI_PASSWORD'))

print("Connected to WiFi")
pool = socketpool.SocketPool(wifi.radio)
requests = adafruit_requests.Session(pool, ssl.create_default_context())

current_time = get_time()

# you must set year, mon, date, hour, min, sec and weekday
t = time.struct_time((current_time[0], current_time[1], current_time[2], current_time[3], current_time[4], current_time[5], current_time[6],   -1,    -1))
#t = time.struct_time((current_time[0], current_time[1], 10, 22, current_time[4], current_time[5], current_time[6],   -1,    -1))

# yearday is not supported, isdst can be set but we don't do anything with it at this time
print("Setting time to:", t)     # uncomment for debugging

rtc.datetime = t
    
CHIME_TIME = 15 #minutes
CHIME_AMOUNT = 3 # Number of times to chime when not on the hour
chimed = False

orientation = False
prev_orientation = False

max_brightness = 1
pointx = 0

BEDTIME = 23
is_after_sunset = False
is_sleep_time = False

first_run = True


    
def get_is_sleep_time(t, weatherReponse):
    is_sleep_time = t.tm_hour >= BEDTIME or now_in_unix < weatherResponse["sunrise"]
    is_before_sunrise = now_in_unix < weatherResponse["sunrise"]
    is_after_sunrise = now_in_unix > weatherResponse["sunrise"]
    
    is_after_sunrise_prev_day = t.tm_hour < time.localtime(weatherResponse["sunrise"]).tm_hour
    print("is_before_sunrise", is_before_sunrise)
    print("is_after_sunrise", is_after_sunrise)
    print("is_after_sunrise_prev_day", is_after_sunrise_prev_day)
    
    if is_before_sunrise or is_after_sunrise and t.tm_hour < time.localtime(weatherResponse["sunrise"]).tm_hour:
        is_sleep_time = True
        print("is after bedtime, and before the sunrise hour the previous day")
    print("is_sleep_time", is_sleep_time)  
    return is_sleep_time

while True:
    t = rtc.datetime
    #print("The date is %d/%d/%d" % (t.tm_mday, t.tm_mon, t.tm_year))
    
    #print("The time is %d:%02d:%02d" % (t.tm_hour, t.tm_min, t.tm_sec))
    
    # getTiltPos returns true if tilt sensor is active (i.e. loop lamp is vertical)
    orientation = getTiltPos()

    do_chime = t.tm_min % CHIME_TIME == 0
    now_in_unix = int(time.mktime(t))
    
    
    
    if(max_brightness < 255):
        max_brightness += 5
        
    if(orientation):
        pointx += 0.1
        
        if pointx > num_pixels:
            pointx = 0
            
        #If we're chiming...
        if(do_chime != chimed):
            print("chiming", str(t.tm_hour) + ':' + str(t.tm_min))
            max_brightness = 1
            weatherResponse = get_weather()
            
            current_weather = weatherResponse["weather"]
            is_after_sunset = now_in_unix > weatherResponse["sunset"]
           
            # Assume weatherResponse["sunrise"] is for today, but it often returns the sunrise time for yesterday
            
                
             # If the hour is passed bedtime (after BEDTIME var) OR is the current time BEFORE sunrise
            is_sleep_time = get_is_sleep_time(t, weatherResponse)
            
            if(t.tm_hour != prev_hour):
                chime_amount = t.tm_hour % 12
            
        
        #If we've just changed orientation of lamp
        if(orientation != prev_orientation):
            print("Flipped")
            
            
            #Get the weather again
            weatherResponse = get_weather()
            
            current_weather = weatherResponse["weather"]
            is_after_sunset = now_in_unix > weatherResponse["sunset"]
            max_brightness = 1
            is_sleep_time = get_is_sleep_time(t, weatherResponse)
           
            
       
        
        #print("Should I be asleep? ", is_sleep_time)
            
        chime(pixels, do_chime and not is_sleep_time, CHIME_AMOUNT)
        
        if is_sleep_time:
            pixels.fill((0,0,0))
        elif is_after_sunset:
            weather_effect(pixels, max_brightness, 'Night', pointx)
        else:
            weather_effect(pixels, max_brightness, current_weather, pointx)
            
        #pixels.show()
       
    else:
        reading_light(pixels)
    
    prev_min = t.tm_min
    prev_hour = t.tm_hour
    
    prev_orientation = orientation
    chimed = do_chime
    first_run = False
#time.sleep(1)
        
    
        
    