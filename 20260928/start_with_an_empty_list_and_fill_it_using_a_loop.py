from machine import Pin
import time

def flash(pin_no, times):
    led_controller = Pin(pin_no, Pin.OUT, value=0)
    speeds = []
    for i in range(times):
        speeds.append(600-i*100)
        
    print(speeds)
    
    for speed  in speeds:
        led_controller.value(1)
        time.sleep_ms(speed)
        led_controller.value(0)
        time.sleep_ms(300)
    
flash(4, 6)
    
