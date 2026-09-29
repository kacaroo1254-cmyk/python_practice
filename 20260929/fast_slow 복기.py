from machine import Pin
import time

flash = Pin(4, Pin.OUT, value=0)
red = Pin(33, Pin.OUT, value=1)

slow = []
fast = []

a=10

for i in range(a):
    slow.append(i*100)
    fast.append(a*100 - i*100)

def run_pattern(pin_obj, pattern_list, ON, OFF):
    for ms in pattern_list:
        pin_obj.value(ON)
        time.sleep_ms(ms)
        pin_obj.value(OFF)
        time.sleep_ms(ms)

run_pattern(red, slow, 0, 1)
run_pattern(red, fast, 0, 1)
