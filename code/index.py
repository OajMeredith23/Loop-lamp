import busio
import adafruit_pcf8523
import time
import board
import digitalio

from tilt import getTiltPos
from chime import chime
from reading_light import reading_light
from weather import weather_light

import neopixel


# Update this to match the number of NeoPixel LEDs connected to your board.
num_pixels = 26

pixels = neopixel.NeoPixel(board.GP6, num_pixels)

    
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

myI2C = busio.I2C(scl=board.GP1, sda=board.GP0)
rtc = adafruit_pcf8523.PCF8523(myI2C)

days = ("Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday")

if False:   # change to True if you want to write the time!
    #                     year, mon, date, hour, min, sec, wday, yday, isdst
    t = time.struct_time((2023,  03,   23,   21,  39,  45,    3,   -1,    -1))
    # you must set year, mon, date, hour, min, sec and weekday
    # yearday is not supported, isdst can be set but we don't do anything with it at this time
    
    print("Setting time to:", t)     # uncomment for debugging
    rtc.datetime = t
    print() 
    
prev_min = 0
prev_hour = 0
while True:
    t = rtc.datetime
    #print(t)     # uncomment for debugging

    #print("The date is %s %d/%d/%d" % (days[t.tm_wday], t.tm_mday, t.tm_mon, t.tm_year))
    print("The time is %d:%02d:%02d" % (t.tm_hour, t.tm_min, t.tm_sec))
    
    is_vertical = getTiltPos()
    #getTiltPos returns true if tilt sensor is active (i.e. loop lamp is vertical)
    if(is_vertical):
        chime_amount = 3
        if(prev_hour != t.tm_hour):
            chime_amount = t.tm_hour % 12
        print("chime_amount", chime_amount)
        weather_light(pixels)
        chime(pixels, t.tm_min % 30 == 0, chime_amount)
    else:
        reading_light(pixels)
    
    prev_min = t.tm_min
    prev_hour = t.tm_hour
    time.sleep(1)
        
    
        
    