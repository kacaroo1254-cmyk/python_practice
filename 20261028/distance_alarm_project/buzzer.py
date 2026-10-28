from machine import Pin, PWM


class Buzzer:
    """PWM 부저의 음량과 켜기/끄기를 담당하는 클래스."""

    DUTY_TABLE = [
        10, 12, 15, 19, 23,
        28, 35, 43, 52, 65,
        79, 98, 120, 148, 182,
        224, 275, 338, 416, 512
    ]

    def __init__(self, pin, freq=880):
        self.pwm = PWM(Pin(pin), freq=freq, duty=0)

    def set_level(self, level):
        level = max(1, min(len(self.DUTY_TABLE), int(level)))
        self.pwm.duty(self.DUTY_TABLE[level - 1])

    def on(self, level):
        self.set_level(level)

    def off(self):
        self.pwm.duty(0)

    def deinit(self):
        self.off()
        self.pwm.deinit()
