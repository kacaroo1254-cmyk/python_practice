import machine
import time
from machine import Pin, PWM, Timer


# ==================================================
# 1. 초음파 센서 클래스
# 역할: 초음파 센서로 거리를 측정한다.
# ==================================================
class UltrasonicSensor:
    def __init__(self, trigger_pin, echo_pin):
        # self.trigger와 self.echo는 이 센서 객체가 기억하는 핀이다.
        self.trigger = Pin(trigger_pin, mode=Pin.OUT, pull=None)
        self.echo = Pin(echo_pin, mode=Pin.IN, pull=None)
        self.trigger.value(0)

    def get_distance_cm(self):
        # 초음파 발사 준비
        self.trigger.value(0)
        time.sleep_us(5)

        # 초음파 발사
        self.trigger.value(1)
        time.sleep_us(10)
        self.trigger.value(0)

        # 에코 핀이 HIGH인 시간 측정
        pulse_time = machine.time_pulse_us(self.echo, 1, 30000)

        # 측정 실패 시 0 반환
        if pulse_time <= 0:
            return 0

        # 왕복 시간을 편도 거리로 변환
        distance_cm = (pulse_time / 2) / 29.1

        # 유효한 거리만 반환
        if 2 <= distance_cm <= 200:
            return distance_cm

        return 0


# ==================================================
# 2. 부저 클래스
# 역할: PWM 음량을 설정하고 소리를 켜거나 끈다.
# ==================================================
class Buzzer:
    DUTY_TABLE = [
        10, 12, 13, 15, 18,
        20, 24, 27, 31, 36,
        42, 48, 55, 64, 73,
        85, 98, 113, 130, 150
    ]

    def __init__(self, pin, freq=880):
        self.pwm = PWM(Pin(pin), freq=freq, duty=0)

    def set_level(self, level):
        # level 1~20을 실제 PWM duty 값으로 변환
        level = max(1, min(len(self.DUTY_TABLE), int(level)))
        self.pwm.duty(self.DUTY_TABLE[level - 1])

    def on(self, level):
        # 지정한 음량으로 부저 켜기
        self.set_level(level)

    def off(self):
        # 부저 끄기
        self.pwm.duty(0)

    def deinit(self):
        # PWM 자원 정리
        self.pwm.duty(0)
        self.pwm.deinit()


# ==================================================
# 3. 거리 알람 클래스
# 역할: 거리 단계를 계산하고 삑삑 패턴을 결정한다.
# ==================================================
class DistanceAlarm:
    def __init__(self, buzzer):
        self.buzzer = buzzer

        # 거리 설정
        self.NEAR_CM = 5
        self.FAR_CM = 40
        self.LEVELS = 20

        # 현재 상태
        self.level = 10
        self.phase = 0
        self.beep_on = False

    def distance_level(self, cm):
        # 가까울수록 높은 단계가 되도록 계산
        level = (
            (self.FAR_CM - cm) * self.LEVELS
            // (self.FAR_CM - self.NEAR_CM)
            + 1
        )

        return max(1, min(self.LEVELS, int(level)))

    def update_distance(self, cm):
        # 유효한 거리일 때만 현재 단계 변경
        if cm != 0:
            self.level = self.distance_level(cm)

    def update_pattern(self):
        # 원래 코드의 10ms 패턴 제어 로직
        if self.level <= 5:
            # 단계가 낮으면 연속음
            self.beep_on = True
            self.phase = 0
        else:
            # 가까울수록 켜짐 시간은 짧아지고 반복 속도는 빨라진다.
            self.phase += 10

            on_time = 40 + (20 - self.level) * 5
            off_time = 250 + (20 - self.level) * 10

            if self.phase < on_time:
                self.beep_on = True
            elif self.phase < on_time + off_time:
                self.beep_on = False
            else:
                self.phase = 0
                self.beep_on = True

        # 결정한 상태를 부저에 전달
        if self.beep_on:
            self.buzzer.on(self.level)
        else:
            self.buzzer.off()


# ==================================================
# 4. 타이머 인터럽트
# 역할: 1ms마다 플래그를 설정한다.
# ==================================================
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


# ==================================================
# 5. 객체 생성
# 클래스에 적힌 설계도를 바탕으로 실제 객체를 만든다.
# ==================================================
sensor = UltrasonicSensor(17, 1)
buzzer = Buzzer(6, freq=880)
alarm = DistanceAlarm(buzzer)

cm = 0
look_gap = 0
last_look = 0

tmr = Timer(0)
tmr.init(period=1, mode=Timer.PERIODIC, callback=tick)


# ==================================================
# 6. 메인 실행부
# 역할: 주기에 맞춰 센서와 알람 객체를 연결한다.
# ==================================================
try:
    while True:

        # 10ms마다 알람 패턴 갱신
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
