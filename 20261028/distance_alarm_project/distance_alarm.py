class DistanceAlarm:
    """거리값을 알람 단계와 소리 패턴으로 변환하는 클래스."""

    def __init__(self, buzzer):
        # 다른 파일에서 만든 Buzzer 객체를 전달받는다.
        self.buzzer = buzzer

        self.NEAR_CM = 5
        self.FAR_CM = 40
        self.LEVELS = 20

        self.level = 10
        self.phase = 0
        self.beep_on = False

    def distance_level(self, cm):
        level = (
            (self.FAR_CM - cm) * self.LEVELS
            // (self.FAR_CM - self.NEAR_CM)
            + 1
        )
        return max(1, min(self.LEVELS, int(level)))

    def update_distance(self, cm):
        # 측정 실패(0)라면 이전 단계를 유지한다.
        if cm != 0:
            self.level = self.distance_level(cm)

    def update_pattern(self):
        # 기존 코드의 10ms 패턴 제어 로직
        if self.level <= 5:
            # 단계가 낮으면 연속음
            self.beep_on = True
            self.phase = 0
        else:
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

        if self.beep_on:
            self.buzzer.on(self.level)
        else:
            self.buzzer.off()
