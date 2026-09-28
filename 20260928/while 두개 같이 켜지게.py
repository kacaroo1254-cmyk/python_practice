from machine import Pin
import time

def blink_both(times, on, off):
    led4 = Pin(4, Pin.OUT, value=0)
    led33 = Pin(33, Pin.OUT, value=1)
    
    count = 0
    
    while count < times:
        led4.value(1)
        led33.value(0)
        time.sleep_ms(on)
        
        led4.value(0)
        led33.value(1)
        time.sleep_ms(off)
        
        count += 1
        
blink_both(3, 200, 600)