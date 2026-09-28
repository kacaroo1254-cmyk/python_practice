from machine import Pin
import time

flash = Pin(4, Pin.OUT, value=0)

speeds = []
a = 10
for i in range(a):
    speeds.append(a*100 - i * 100)
print(speeds)

for ms in speeds:
    flash.value(1)
    time.sleep_ms(ms//2)
    flash.value(0)
    time.sleep_ms(ms//2)