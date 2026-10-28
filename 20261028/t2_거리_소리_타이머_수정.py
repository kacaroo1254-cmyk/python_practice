
import machine
import time
from machine import Pin, PWM, Timer

# ---- 부저와 초음파 센서 설정 ----
buzzer = PWM(Pin(6), freq=880, duty=0)

trigger = Pin(17, mode=Pin.OUT, pull=None)
echo = Pin(1, mode=Pin.IN, pull=None)

trigger.value(0)

# ---- 내가 바꾸는 값 ----
NEAR_CM = 5
FAR_CM = 100
LEVELS = 20

US_PER_CM = 29.1
TIMEOUT_MARGIN = 1.2

# FAR_CM에 따라 초음파 측정 제한시간을 자동 계산
# 거리(cm) × 왕복 시간 × 여유 비율
TIMEOUT_US = int(FAR_CM * 2 * US_PER_CM * TIMEOUT_MARGIN)

DUTY_TABLE = [
    10, 12, 13, 15, 18, 20, 24, 27, 31, 36,
    42, 48, 55, 64, 73, 85, 98, 113, 130, 150
]

# ---- 인터럽트 깃발 ----
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


def get_distance_cm():
    # 초음파 발사 준비
    trigger.value(0)
    time.sleep_us(5)

    # 초음파 발사 신호
    trigger.value(1)
    time.sleep_us(10)
    trigger.value(0)

    # Echo 신호가 켜져 있는 시간 측정
    pulse_time = machine.time_pulse_us(
        echo, 1, TIMEOUT_US
    )

    # 시간 초과 또는 측정 실패
    if pulse_time < 0:
        return 0

    # 왕복 시간을 편도 시간으로 바꿔 거리 계산
    distance_cm = (pulse_time / 2) / US_PER_CM

    # 소리 단계의 기준 거리만 허용
    if NEAR_CM <= distance_cm <= FAR_CM:
        return distance_cm

    return 0


def distance_level(cm):
    # 거리를 소리 단계 번호로 변환
    level = int(
        (FAR_CM - cm) * LEVELS // (FAR_CM - NEAR_CM)
    )

    # 단계 번호가 유효한 범위를 벗어나지 않도록 보호
    if level < 0:
        level = 0

    if level > LEVELS - 1:
        level = LEVELS - 1

    return level


# ---- 초기 상태 ----
beep_on = False
cm = 0
level = 9
duty = DUTY_TABLE[level]

# ---- 타이머 시작 ----
tmr = Timer(0)
tmr.init(
    period=1,
    mode=Timer.PERIODIC,
    callback=tick
)

try:
    while True:

        # 10ms마다 부저 출력 반영
        if flag_10:
            flag_10 = False

            if beep_on:
                buzzer.duty(duty)
            else:
                buzzer.duty(0)

        # 50ms마다 거리 측정
        if flag_50:
            flag_50 = False

            cm = get_distance_cm()

            # 측정에 성공한 경우에만 단계 갱신
            if cm != 0:
                level = distance_level(cm)
                duty = DUTY_TABLE[level]

        # 500ms마다 부저 상태 변경 및 출력
        if flag_500:
            flag_500 = False

            beep_on = not beep_on

            print(
                "거리", int(cm), "cm",
                "-> 단계", level,
                "-> duty", duty
            )

except KeyboardInterrupt:
    pass

finally:
    # 타이머와 부저 정리
    tmr.deinit()
    buzzer.duty(0)
    buzzer.deinit()
