from machine import Pin, PWM, Timer
import time

M1_motor = PWM(Pin(4), freq=10000, duty=0)
M2_motor = PWM(Pin(5), freq=10000, duty=0)
M3_motor = PWM(Pin(40), freq=10000, duty=0)
M4_motor = PWM(Pin(41), freq=10000, duty=0)

ms_flag = False
time_cnt = 0

duty_cnt = [30, 60, 90, 120, 150]
step = 0
direction = 1

def timer_callback(t):
    global ms_flag
    ms_flag = True

def timer_10ms():
    global step, direction

    if time_cnt % 1000 == 0:
        duty = duty_cnt[step]
        print("단계: {}, 시간ms: {}, PWM: {}".format (step+1, time_cnt, duty))
        M1_motor.duty(duty)
        M2_motor.duty(duty)
        M3_motor.duty(duty)
        M4_motor.duty(duty)
        step += direction
        

        if step >= len(duty_cnt) - 1:
            step = len(duty_cnt) - 1
            direction = -1

        elif step <= 0:
            step = 0
            direction = 1

tmr = Timer(0)
tmr.init(period=1, mode=Timer.PERIODIC, callback=timer_callback)

try:
    while True:
        if ms_flag:
            ms_flag = False
            time_cnt += 1

            if time_cnt % 10 == 0:
                timer_10ms()

except KeyboardInterrupt:
    M1_motor.deinit()
    M2_motor.deinit()
    M3_motor.deinit()
    M4_motor.deinit()
    tmr.deinit()
    print("코드를 종료합니다.")
