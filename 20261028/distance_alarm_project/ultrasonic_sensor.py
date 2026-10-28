import machine
import time
from machine import Pin


class UltrasonicSensor:
    """초음파 센서로 거리를 측정하는 클래스."""

    def __init__(self, trigger_pin, echo_pin):
        self.trigger = Pin(trigger_pin, mode=Pin.OUT, pull=None)
        self.echo = Pin(echo_pin, mode=Pin.IN, pull=None)
        self.trigger.value(0)

    def get_distance_cm(self):
        self.trigger.value(0)
        time.sleep_us(5)

        self.trigger.value(1)
        time.sleep_us(10)
        self.trigger.value(0)

        pulse_time = machine.time_pulse_us(self.echo, 1, 30000)

        if pulse_time <= 0:
            return 0

        distance_cm = (pulse_time / 2) / 29.1

        if 2 <= distance_cm <= 200:
            return distance_cm

        return 0
