from machine import Pin
import time

led4 = Pin(4, Pin.OUT, value=0)
led33 = Pin(33, Pin.OUT, value=1)


def blink(pin_no, times, on):
    n = 1
    for i in range(times):
        if i == 3 * n - 1:
            led33.value(1 - on)
            time.sleep_ms(300)
            led33.value(on)
            n += 1
        else:
            pin_no.value(on)
            time.sleep_ms(300)
            pin_no.value(1 - on)
            time.sleep_ms(300)
        print(i)
        
blink(led4, 10, 1)

    