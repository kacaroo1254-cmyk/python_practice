from machine import Pin
import time

flash = Pin(4, Pin.OUT, value=0)
red = Pin(33, Pin.OUT, value=1)

def make_speedup(count, start, step):
    result = []
    for i in range(count):
        result.append(start - i * step)
    return result

fast = make_speedup(6, 600, 100)
print(fast)