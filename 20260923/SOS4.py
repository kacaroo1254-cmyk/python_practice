from machine import Pin
import time

flash = Pin(4, Pin.OUT, value=0)

def blink_once(times, on, off):
    for _ in range(times):
        flash.value(1)
        time.sleep_ms(on)
        flash.value(0)
        time.sleep_ms(off)
    
blink_once(3, 300, 900)
blink_once(3, 600, 100)