from machine import Pin
import time

flash = Pin(4, Pin.OUT, value=0)

UNIT = 150
LOVE = [1, 3, 1, 1, 3, 3, 3, 1, 1, 1, 3, 1]

def morse_luv(pin_obj, signals, unit):
    for s in signals:
        pin_obj.value(1)
        time.sleep_ms(s * unit)
        pin_obj.value(0)
        time.sleep_ms(unit)
        
morse_luv(flash, LOVE, UNIT)
print("LOVE 전송완료")