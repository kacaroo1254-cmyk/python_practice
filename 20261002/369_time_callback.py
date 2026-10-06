from machine import Pin, Timer
import time

flash = Pin(4, Pin.OUT, value= 0)
red = Pin(33, Pin.OUT, value= 1)


def blink_red():
    red.value(0)
    time.sleep_ms(250)
    red.value(1)

def blink_flash():
    flash.value(1)
    red.value(0)
    time.sleep_ms(250)
    red.value(1)
    flash.value(0)


def timer_callback(t):
    global ms_flag
    ms_flag = True

i = 1
ms_flag = False
tmr = Timer(0)

tmr.init(
    period=1000,
    mode=Timer.PERIODIC,
    callback=timer_callback
)

try:
    while True:
        if ms_flag:
            ms_flag = False

            print (i)
            if i < 10:
                if i % 3 == 0:
                    blink_flash()
                    print('짝!')
                else:
                    blink_red()
            elif i < 100:
                first_num = int(i/10)
                second_num = i % 10
                if first_num % 3 == 0:
                    blink_flash()
                    print('짝!')
                if second_num % 3 == 0 and second_num!= 0:
                    blink_flash()
                    print('짝!')
                else:
                    blink_red()
            else:
                first_num = int(i/100)
                second_num = int((i - (first_num * 100)) / 10)
                third_num = (i - (first_num * 100)) % 10
                if first_num % 3 == 0:
                    blink_flash()
                    print('짝!')
                if second_num % 3 == 0 and second_num!= 0:
                    blink_flash()
                    print('짝!')
                if third_num % 3 == 0 and third_num!= 0:
                    blink_flash()
                    print('짝!')
                else:
                    blink_red()

            i += 1


except KeyboardInterrupt:
    flash.value(0)
    red.value(1)
    tmr.deinit()
    print("타이머 정지")
