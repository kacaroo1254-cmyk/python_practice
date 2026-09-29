from machine import Pin
import time

flash = Pin(4, Pin.OUT, value=0)
red = Pin(33, Pin.OUT, value=1)

leds = [flash, red]
ON = [1, 0]
OFF = [0, 1]

for i in range(len(leds)):
    print(i, "번 LED 켜기")
    leds[i].value(ON[i])
    time.sleep_ms(500)
    leds[i].value(OFF[i])
       
       