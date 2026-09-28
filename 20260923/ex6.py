from machine import Pin
import time

def blink_flash(pin_no, times, on, off):
    
    if pin_no == 4 :
        ON = 1
        OFF = 0
    else :
        ON = 0
        OFF = 1

    led_controller = Pin(pin_no, Pin.OUT, value=0)
    for _ in range(times):
        led_controller.value(ON)
        time.sleep_ms(on)
        led_controller.value(OFF)
        time.sleep_ms(off)
        

blink_flash(4, 3, 300, 500)
blink_flash(33, 3, 100, 900)