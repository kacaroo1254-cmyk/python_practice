ms_time = [100, 300, 500, 700, 900]
print(ms_time[2])
print(ms_time[4])

from machine import Pin
import time

def flash(pin_no, times, ms_on, ms_off):
    if pin_no == 4:
        on = 1
        off = 0
    else :
        on = 0
        off = 1
    for _ in range(times):
        led_controller = Pin(pin_no, Pin.OUT, value=0)
        led_controller.value(on)
        time.sleep_ms(ms_on)
        led_controller.value(off)
        time.sleep_ms(ms_off)
            
flash(4, 3, ms_time[3], ms_time[1])
flash(33, 3, ms_time[3], ms_time[1])