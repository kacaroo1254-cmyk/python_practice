
from machine import Pin, PWM, Timer
import bluetooth, ble_simple_peripheral, time

ble = bluetooth.BLE()
p = ble_simple_peripheral.BLESimplePeripheral(
    ble, name='pyD_2344'
)

# 모터 PWM 초기화
M1_motor = PWM(Pin(4), freq=10000, duty=0)
M2_motor = PWM(Pin(5), freq=10000, duty=0)
M3_motor = PWM(Pin(40), freq=10000, duty=0)
M4_motor = PWM(Pin(41), freq=10000, duty=0)

# 스마트폰에서 받은 속도 단계 (1~5)
value = 1

# 타이머 변수
ms_flag = False
time_cnt = 0

# 속도 단계별 PWM 출력값
duty_cnt = [30, 60, 90, 120, 150]


# BLE 데이터 수신 함수
def on_rx(read):
    global value

    try:
        if isinstance(read, bytes):
            read = read.decode().strip()
        else:
            read = str(read).strip()

        new_value = int(read)

        if 1 <= new_value <= 5:
            value = new_value
            print("속도 단계:", value)
        else:
            print("1~5 사이의 숫자를 보내세요.")

    except (ValueError, UnicodeError):
        print("숫자를 입력해 주세요:", read)


p.on_write(on_rx)


# 타이머 인터럽트 콜백
def timer_callback(t):
    global ms_flag
    ms_flag = True


# 10ms마다 실행할 함수
def timer_10ms():
    global value

    # 1000ms마다 모터 출력 변경
    if time_cnt % 1000 == 0:
        duty = duty_cnt[value - 1]

        M1_motor.duty(duty)
        M2_motor.duty(duty)
        M3_motor.duty(duty)
        M4_motor.duty(duty)

        print("duty:", duty)


# 1ms 주기 타이머
tmr = Timer(0)
tmr.init(
    period=1,
    mode=Timer.PERIODIC,
    callback=timer_callback
)

try:
    while True:
        if ms_flag:
            ms_flag = False
            time_cnt += 1

            if time_cnt % 10 == 0:
                timer_10ms()

except KeyboardInterrupt:
    tmr.deinit()

    M1_motor.deinit()
    M2_motor.deinit()
    M3_motor.deinit()
    M4_motor.deinit()

    print("코드를 종료합니다.")

