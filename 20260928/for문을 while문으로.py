from machine import Pin
import time

def blink(pin_no, times, on, off):
    if pin_no == 4 :
        ON = True
        OFF = False
    else :
        OFF = True
        ON = False
        
    led_controller = Pin(pin_no, Pin.OUT, value=0)
    
    count = 0
        
    while count < times:
            led_controller.value(ON)
            time.sleep_ms(on)
            led_controller.value(OFF)
            time.sleep_ms(off)
            
            count += 1

blink(4, 3, 300, 500)
blink(33,3, 100, 900)