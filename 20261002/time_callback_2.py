from machine import Pin, Timer

flash = Pin(4, Pin.OUT, value=0)
red = Pin(33, Pin.OUT, value=1)

time_cnt = 0
ms_flag = False
tmr = Timer(0)


def timer_100ms():
    flash.value(flash.value() ^ 1)


def timer_500ms():
    red.value(red.value() ^ 1)


def timer_callback(t):
    global ms_flag
    ms_flag = True


tmr.init(
    period=1000,
    mode=Timer.PERIODIC,
    callback=timer_callback
)

try:
    while True:
        if ms_flag:
            ms_flag = False
            time_cnt += 1
            print(time_cnt)

            if time_cnt % 1 == 0:
                timer_100ms()

            if time_cnt % 5 == 0:
                timer_500ms()


except KeyboardInterrupt:
    flash.value(0)
    red.value(1)
    tmr.deinit()
    print("타이머 정지")
