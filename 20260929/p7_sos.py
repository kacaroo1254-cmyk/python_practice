from machine import Pin
import time

flash = Pin(4, Pin.OUT, value=0)

UNIT = 150
SOS = [1, 1, 1, 3, 3, 3, 1, 1, 1]

def send_morse(pin_obj, signals, unit):
    for s in signals:
        pin_obj.value(1)
        time.sleep_ms(s * unit)
        pin_obj.value(0)
        time.sleep_ms(unit)
        
send_morse(flash, SOS, UNIT)
print("SOS 전송완료")