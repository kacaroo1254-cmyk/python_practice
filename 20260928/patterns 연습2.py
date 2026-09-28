from machine import Pin
import time

flash = Pin(4, Pin.OUT, value=0)
patterns = [300, 100, 600, 100, 300]

flash.value(1)
time.sleep_ms(patterns[2])
flash.value(0)
print("켠시간:", patterns[2])