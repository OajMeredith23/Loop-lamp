import math

chime_i = 0
chiming = True
brightness = 1
MIN_BRIGHTNESS = 0
finished = False
def chime(pixels, action, num_chimes):
    global chime_i
    global chiming
    global brightness
    global finished
    
    if(action == False):
        chime_i = 0
        finished = False
    
    if(action and not finished):
        chiming = True
        prev_brightness = 0
        chimed = 0
        while chiming:
            brightness = max(MIN_BRIGHTNESS, math.floor(((math.sin(chime_i) + 1) / 2) * 255))
            if(brightness != prev_brightness):
                pixels.fill((brightness, 0, 0))
                if(brightness == MIN_BRIGHTNESS):
                    chimed += 1
            if(chimed >= num_chimes):
                chiming = False
            #print("action", action, brightness)
            chime_i += 0.005
            prev_brightness = brightness
            
        finished = True