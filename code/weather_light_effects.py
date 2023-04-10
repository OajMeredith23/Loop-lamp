import math
import os
import time
import random
from rainbowio import colorwheel

num_pixels = os.getenv('num_pixels')

maxbrightness = 255

DIMMER = 3

# out of ten, lower is higher frequency
FLASH_FREQUENCY = {
    "Thunderstorm": 5,
    "Snow" : 5,
    "Rain": 2
    }

# higher is dimmer
FLASH_BRIGHTNESS = {
    "Thunderstorm": 0,
    "Snow" : 0,
    "Rain": 4
    }
# Clear, Clouds, Rain, Drizzle, Thunderstorm, Snow, Mist, Haze, Fog 
def weather_effect(pixels, max_brightness, weather, pointx):
    
    
    show_random_pixel = False
    random_pixel = 0
    random_pixel_color = (0,0,0)
    if (weather == 'Thunderstorm' or weather == 'Snow' or weather == 'Rain') and math.floor(random.random() * 10) > FLASH_FREQUENCY[weather]:
        show_random_pixel = True
        if weather == 'Thunderstorm':
            random_pixel_color = (245 / FLASH_BRIGHTNESS[weather], 235 / FLASH_BRIGHTNESS[weather], 100 / FLASH_BRIGHTNESS[weather])
        if weather == 'Snow':
            random_pixel_color = (255 / FLASH_BRIGHTNESS[weather], 255 / FLASH_BRIGHTNESS[weather], 255 / FLASH_BRIGHTNESS[weather])
        if weather == 'Rain':
            random_pixel_color = (50 / FLASH_BRIGHTNESS[weather], 150  / FLASH_BRIGHTNESS[weather], 255 / FLASH_BRIGHTNESS[weather])
        random_pixel = math.floor(random.random() * num_pixels)
        
    for x in range(num_pixels):
        distFromLightPos1 = abs(pointx - x)
        distFromLightPos2 = abs(pointx - x + num_pixels)
        distFromLightPos3 = abs(pointx - x - num_pixels)
        distFromLightPos = min(distFromLightPos1, min(distFromLightPos2, distFromLightPos3))
        brightness = round(max(255 - distFromLightPos * 40, 0))
        
        r = (round(brightness))
        g = 100
        b = 100
        
        if(weather == 'Clouds' or weather == 'Thunderstorm' or weather == 'Snow'):
            r = round(brightness)
            g = round(brightness)
            b = round(brightness)
            
        if(weather == 'Rain'):
            r = round(brightness/2)
            g = round(brightness / 3)
            b = 50
            
        if(weather == 'Night'):
            r = 255
            g = max(0, 155 - brightness)
            b = 50
        
            
        pixels[x] = (min(max_brightness, r), min(max_brightness, g), min(max_brightness, b))
        if(show_random_pixel):
            pixels[random_pixel] = random_pixel_color
        
