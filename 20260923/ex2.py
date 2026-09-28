from machine import Pin
import time

ON = True
OFF = False

def blink_once(times, on, off):
    flash = Pin(4, Pin.OUT, value=0)
    for _ in range(times):
        flash.value(1)
        time.sleep_ms(on)
        flash.value(0)
        time.sleep_ms(off)
        
blink_once(3, 300, 500)
blink_once(3, 100, 900)
