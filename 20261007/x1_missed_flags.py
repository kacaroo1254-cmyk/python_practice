from machine import Pin, Timer
import time

flash = Pin(4, Pin.OUT, value=0)
red = Pin(33, Pin.OUT, value=1)

flag_10ms = False
flag_100ms = False
flag_500ms = False
flag_1000ms = False

missed_100 = 0   # 깃발이 아직 서 있는데 또 올리려던 횟수 (놓친 눈금)
isr_cnt = 0

def timer_isr(t):
    global isr_cnt, flag_10ms, flag_100ms, flag_500ms, flag_1000ms, missed_100
    isr_cnt += 1
    if isr_cnt % 10 == 0:
        flag_10ms = True
    if isr_cnt % 100 == 0:
        if flag_100ms:          # 아직 안 내려갔다 = 메인이 못 따라왔다
            missed_100 += 1
        flag_100ms = True
    if isr_cnt % 500 == 0:
        flag_500ms = True
    if isr_cnt >= 1000:
        flag_1000ms = True
        isr_cnt = 0

def task_10ms():
    pass

def task_100ms():
    flash.value(flash.value() ^ 1)

def task_500ms():
    red.value(red.value() ^ 1)
    time.sleep_ms(300)

def task_1000ms():
    global missed_100
    print("놓친 100ms 깃발:", missed_100)
    missed_100 = 0

tmr = Timer(0)
tmr.init(period=1, mode=Timer.PERIODIC, callback=timer_isr)

try:
    while True:
        if flag_10ms:
            flag_10ms = False
            task_10ms()
        if flag_100ms:
            flag_100ms = False
            task_100ms()
        if flag_500ms:
            flag_500ms = False
            task_500ms()
        if flag_1000ms:
            flag_1000ms = False
            task_1000ms()
except KeyboardInterrupt:
    tmr.deinit()
    flash.value(0)
    red.value(1)
    print("타이머 정지")
