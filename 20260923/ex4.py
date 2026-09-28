from machine import Pin
import time

ON = True
OFF = False

def blink_flash(times, LED, on, off):
    flash = Pin(LED, Pin.OUT, value=0)
    for _ in range(times):
        flash.value(ON)
        time.sleep_ms(on)
        flash.value(OFF)
        time.sleep_ms(off)
        

blink_flash(3, 4, 300, 500)
blink_flash(3, 33, 100, 900)