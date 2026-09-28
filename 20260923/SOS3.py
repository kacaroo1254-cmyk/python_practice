from machine import Pin
import time

flash = Pin(33, Pin.OUT, value=0)

ON = 0
OFF = 1

def blink_once(times, on, off):
    for _ in range(times):
        flash.value(ON)
        time.sleep_ms(on)
        flash.value(OFF)
        time.sleep_ms(off)
        
blink_once(3, 300, 900)
blink_once(3, 100, 100)


