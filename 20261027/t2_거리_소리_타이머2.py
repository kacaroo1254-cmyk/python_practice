import machine
import time
from machine import Pin, PWM, Timer

# 부저 설정
buzzer = PWM(Pin(6), freq=880, duty=0)

# 초음파 센서 설정
trigger = Pin(17, mode=Pin.OUT, pull=None)
echo = Pin(1, mode=Pin.IN, pull=None)
trigger.value(0)

# ---- 거리 및 음량 설정 ----
NEAR_CM = 5
FAR_CM = 40
LEVELS = 20

DUTY_TABLE = [
    10, 12, 15, 19, 23,
    28, 35, 43, 52, 65,
    79, 98, 120, 148, 182,
    224, 275, 338, 416, 512
]

# ---- 타이머 인터럽트 설정 ----
ms = 0
flag_10 = False
flag_50 = False
flag_500 = False

def tick(t):
    global ms, flag_10, flag_50, flag_500

    ms += 1

    if ms % 10 == 0:
        flag_10 = True

    if ms % 50 == 0:
        flag_50 = True

    if ms % 500 == 0:
        flag_500 = True


# ---- 거리 측정 함수 ----
def get_distance_cm():
    trigger.value(0)
    time.sleep_us(5)

    trigger.value(1)
    time.sleep_us(10)
    trigger.value(0)

    pulse_time = machine.time_pulse_us(echo, 1, 30000)

    # 측정 실패 시 0 반환
    if pulse_time <= 0:
        return 0

    distance_cm = (pulse_time / 2) / 29.1

    if 2 <= distance_cm <= 200:
        return distance_cm
    else:
        return 0


# ---- 거리를 음량 단계로 변환 ----
def distance_level(cm):
    level = (FAR_CM - cm) * LEVELS // (FAR_CM - NEAR_CM) + 1

    return max(1, min(LEVELS, int(level)))


# ---- 초기 상태 ----
beep_on = False
cm = 0
level = 10
duty = DUTY_TABLE[level - 1]

last_look = 0
look_gap = 0

# 소리 패턴 제어 변수
phase = 0

# 타이머 시작: 1ms마다 tick 실행
tmr = Timer(0)
tmr.init(period=1, mode=Timer.PERIODIC, callback=tick)

try:
    while True:

        # ---- 10ms마다 소리 패턴 제어 ----
        if flag_10:
            flag_10 = False

            # 가까울수록 삑삑, 멀수록 연속음
            if level <= 5:
                # 먼 거리: 연속음
                beep_on = True
                phase = 0

            else:
                # 가까운 거리: 삑삑 소리
                phase += 10

                # 가까울수록 짧게 울리고 빠르게 반복
                on_time = 40 + (20 - level) * 5
                off_time = 250 + (20 - level) * 10

                if phase < on_time:
                    beep_on = True

                elif phase < on_time + off_time:
                    beep_on = False

                else:
                    phase = 0
                    beep_on = True

            # 부저에 음량 적용
            if beep_on:
                buzzer.duty(duty)
            else:
                buzzer.duty(0)

        # ---- 50ms마다 거리 측정 ----
        if flag_50:
            flag_50 = False

            cm = get_distance_cm()

            if cm != 0:
                level = distance_level(cm)
                duty = DUTY_TABLE[level - 1]

            look_gap = ms - last_look
            last_look = ms

        # ---- 500ms마다 상태 출력 ----
        if flag_500:
            flag_500 = False

            print(
                "거리", int(cm), "cm",
                "-> 단계", level,
                "-> duty", duty,
                "| 센서 측정 간격", look_gap, "ms"
            )

except KeyboardInterrupt:
    pass

finally:
    tmr.deinit()
    buzzer.duty(0)
    buzzer.deinit()