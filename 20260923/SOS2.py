from machine import Pin
import time

flash = Pin(4, Pin.OUT, value=0)

def blink_once(ms):
    for _ in range(3):
        flash.value(1)
        time.sleep_ms(ms)
        flash.value(0)
        time.sleep_ms(ms)
    
blink_once(300)