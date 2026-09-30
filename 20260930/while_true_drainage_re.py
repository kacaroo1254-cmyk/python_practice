from machine import Pin
import time

flash = Pin(4, Pin.OUT, value=0)
red = Pin(33, Pin.OUT, value=1)

counter = 1

try:
    while True:
        flash.value(1)
        if(counter % 5 == 0):
            red.value(0)
        time.sleep_ms(500)
        
        flash.value(0)
        if(counter % 5 == 0):
            red.value(1)
        time.sleep_ms(500)
        
        print(counter)
        counter += 1
           
finally:
    flash.value(0)
    red.value(1) 