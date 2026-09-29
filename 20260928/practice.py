from machine import Pin
import time

flash = Pin(4, Pin.OUT, value=0)
red = Pin(33, Pin.OUT, value=1)

slow = []
fast = []

for i in range(3):
    slow.append(800)
    
for i in range(6):
    fast.append(100)
    
    
def run_pattern(pin_obj, pattern_list, ON, OFF):
    for ms in pattern_list:
        pin_obj.value(ON)
        time.sleep_ms(ms)
        pin_obj.value(OFF)
        time.sleep_ms(200)
        
run_pattern(flash, slow, 1, 0)
run_pattern(flash, fast, 1, 0)
run_pattern(red, slow, 0, 1)
run_pattern(red, fast, 0, 1)