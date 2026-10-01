# from machine import Pin
# import time

# flash = Pin(4, Pin.OUT, value=0)
# red = Pin(33, Pin.OUT, value=1)

# counter = 0
# time_cnt = 0
# red_on = 0

# def timer_100ms():
#     flash.value(not flash.value())

# def timer_500ms():
#     red.value(not red.value())

# while True:
#     time.sleep_ms(1)
#     time_cnt += 1

#     if time_cnt % 100 == 0:
#         timer_100ms()

#     if time_cnt % 500 == 0:
#         timer_500ms()

from machine import Pin
import time

flash = Pin(4, Pin.OUT, value=0)

time_cnt = 0
start = time.ticks_ms() #시작 시간(ms)

while time_cnt < 1000:
    time.sleep_ms(1) # 1ms 대기
    time_cnt += 1

    if time_cnt % 100 == 0:
        flash.value(not flash.value())

spent = time.ticks_diff(time.ticks_ms(), start)
print("1ms를 1000번 센시간: ", spent, "ms")
print("목표는 1000ms 입니다. 차이: ", spent - 1000, "ms")
