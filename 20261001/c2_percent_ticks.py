from machine import Pin
import time

flash = Pin(4, Pin.OUT, value=0)
red = Pin(33, Pin.OUT, value=1)

counter = 0
time_cnt = 0

def timer_100ms():
    flash.value(not flash.value())

def timer_300ms():
    red.value(not red.value())

try:
    while True:
        time.sleep_ms(10)
        time_cnt += 1
        
        print(time_cnt)
        
        if time_cnt % 100 == 0:
            timer_100ms()

        if time_cnt % 300 == 0:
            timer_300ms()
finally:
    flash.value(0)
    red.value(1)