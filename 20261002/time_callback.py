from machine import Pin, Timer
import time

flash = Pin(4, Pin.OUT, value=0)
red = Pin(33, Pin.OUT, value=1)

time_cnt = 0
ms_flag = False


def timer_100ms():
    flash.value(flash.value() ^ 1)


def timer_500ms():
    red.value(red.value() ^ 1)

def timer_callback(t):
    global ms_flag
    ms_flag = True

tmr  = Timer(0)
tmr.init(
    period=1,
    mode=Timer.PERIODIC,
    callback=timer_callback
)

try:
    while True:
        if ms_flag:
            ms_flag = False
            time_cnt += 1

            if time_cnt % 100 == 0:
                timer_100ms()

            if time_cnt % 500 == 0:
                timer_500ms()


except KeyboardInterrupt:
    flash.value(0)
    red.value(1)
    tmr.deinit()
    print("타이머 정지")