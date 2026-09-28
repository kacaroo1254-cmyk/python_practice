from machine import Pin
import time

flash = Pin(4, Pin.OUT, value=0)
def s():
    flash.value(1)
    time.sleep_ms(300)
    flash.value(0)
    time.sleep_ms(300)
    
def o():
    flash.value(1)
    time.sleep_ms(900)
    flash.value(0)
    time.sleep_ms(300)
    
try :
    while True:
        s()
        o()
        s()
    
finally:
    flash.value(0)