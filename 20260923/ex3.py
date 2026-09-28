from machine import Pin
import time

ON = True
OFF = False

def blink_flash(times, on, off):
    flash = Pin(4, Pin.OUT, value=0)
    for _ in range(times):
        flash.value(ON)
        time.sleep_ms(on)
        flash.value(OFF)
        time.sleep_ms(off)
        
def blink_led(times, on, off):
    led = Pin(33, Pin.OUT, value=0)
    for _ in range(times):
        led.value(OFF)
        time.sleep_ms(on)
        led.value(ON)
        time.sleep_ms(off)
        
blink_flash(3, 300, 500)
blink_led(3, 100, 900)
