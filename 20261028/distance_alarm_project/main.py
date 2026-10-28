import time
from machine import Timer

from ultrasonic_sensor import UltrasonicSensor
from buzzer import Buzzer
from distance_alarm import DistanceAlarm


# 타이머 플래그
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


# 객체 생성
sensor = UltrasonicSensor(17, 1)
buzzer = Buzzer(6, freq=880)
alarm = DistanceAlarm(buzzer)

cm = 0
look_gap = 0
last_look = 0

tmr = Timer(0)
tmr.init(period=1, mode=Timer.PERIODIC, callback=tick)

try:
    while True:
        # 10ms마다 소리 패턴 갱신
        if flag_10:
            flag_10 = False
            alarm.update_pattern()

        # 50ms마다 거리 측정
        if flag_50:
            flag_50 = False

            cm = sensor.get_distance_cm()
            alarm.update_distance(cm)

            look_gap = ms - last_look
            last_look = ms

        # 500ms마다 상태 출력
        if flag_500:
            flag_500 = False

            duty = buzzer.DUTY_TABLE[alarm.level - 1]

            print(
                "거리", int(cm), "cm",
                "-> 단계", alarm.level,
                "-> duty", duty,
                "| 센서 측정 간격", look_gap, "ms"
            )

except KeyboardInterrupt:
    pass

finally:
    tmr.deinit()
    buzzer.deinit()
