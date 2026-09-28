from machine import Pin
import time

flash = Pin(4, Pin.OUT, value=0)

def blink_once(times, on, off):
    for _ in range(times):
        flash.value(1)
        time.sleep_ms(on)
        flash.value(0)
        time.sleep_ms(off)
def x():
    blink_once(1, 300, 900)
    blink_once(1, 600, 100)

x(2)
