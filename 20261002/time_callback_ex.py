# machine 모듈에서 디지털 입출력을 위한 Pin과 주기적 처리를 위한 Timer 클래스를 가져옵니다.
from machine import Pin, Timer
import time  # 시간 관련 모듈 불러오기

# GPIO 4번 핀을 출력(OUT)으로 설정하고, 초기 상태를 0(LOW/꺼짐)으로 설정합니다. (플래시 LED)
flash = Pin(4, Pin.OUT, value=0)

# GPIO 33번 핀을 출력(OUT)으로 설정하고, 초기 상태를 1(HIGH/켜짐)으로 설정합니다. (빨간색 LED)
red = Pin(33, Pin.OUT, value=1)

# 경과 시간을 카운트할 변수를 0으로 초기화합니다.
time_cnt = 0

# 1ms 타이머 인터럽트가 발생했음을 알리는 플래그 변수입니다.
ms_flag = False

# 타이머 인터럽트가 발생할 때마다 실행될 콜백(Callback) 함수입니다.
def timer_callback(t):
    global ms_flag  # 전역 변수인 ms_flag를 함수 내에서 수정하기 위해 global 선언을 합니다.
    ms_flag = True  # 1ms마다 타이머가 호출되어 깃발(플래그)을 올립니다.

# 100ms마다 실행할 함수: flash LED의 상태를 반전(토글)시킵니다.
def timer_100ms():
    # XOR(^) 연산을 사용하여 현재 값이 0이면 1로, 1이면 0으로 변경합니다.
    flash.value(flash.value() ^ 1)

# 500ms마다 실행할 함수: red LED의 상태를 반전(토글)시킵니다.
def timer_500ms():
    # XOR(^) 연산을 사용하여 현재 값이 0이면 1로, 1이면 0으로 변경합니다.
    red.value(red.value() ^ 1)

# 하드웨어 타이머 0번 객체를 생성합니다.
tmr = Timer(0)

# 타이머를 초기화합니다.
# period=1 (1밀리초 간격), mode=Timer.PERIODIC (주기적 반복), callback=timer_callback (호출할 함수)
tmr.init(period=1, mode=Timer.PERIODIC, callback=timer_callback)

try:
    # 프로그램이 종료되기 전까지 무한 루프를 돌며 동작합니다.
    while True:
        # 1ms 타이머 인터럽트에 의해 ms_flag가 True가 되었는지 확인합니다.
        if ms_flag:
            ms_flag = False  # 다음 1ms 이벤트를 기다리기 위해 플래그를 다시 False로 안착시킵니다.
            time_cnt += 1    # 카운터를 1 감산/증가시킵니다 (1ms 경과).

            # time_cnt가 100의 배수일 때 (100ms 마다) 100ms 동작 함수를 호출합니다.
            if time_cnt % 100 == 0:
                timer_100ms()

            # time_cnt가 500의 배수일 때 (500ms 마다) 500ms 동작 함수를 호출합니다.
            if time_cnt % 500 == 0:
                timer_500ms()
                time_cnt = 0 # 100과 500의 최소공배수인 500에 도달하면 카운터를 0으로 초기화합니다.

except KeyboardInterrupt:
    # 사용자가 Ctrl+C 등을 눌러 프로그램을 강제 종료했을 때 처리하는 구문입니다.
    tmr.deinit()  # 하드웨어 타이머 동작을 안전하게 중지합니다.
    print("타이머 정지")  # 안내 메시지를 출력합니다.