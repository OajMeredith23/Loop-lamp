
import board
import digitalio


tilt_pin = digitalio.DigitalInOut(board.GP10)
tilt_pin.direction = digitalio.Direction.INPUT

def getTiltPos():
    return tilt_pin.value