from machine import Pin, PWM, Timer
import bluetooth,ble_simple_peripheral,time

ble = bluetooth.BLE()
p = ble_simple_peripheral.BLESimplePeripheral(ble,name='pyD_2344')
value = 0

def on_rx(read):
    global value

    print("RX", read)

    try:
        # 받은 데이터를 문자열로 변환
        read = read.decode().strip() if isinstance(read, bytes) else str(read)

        # 문자열을 정수로 변환
        value = int(read)

        print("변환된 duty:", value)

    except ValueError:
        print("숫자를 입력해 주세요:", read)

    return value
    
    
p.on_write(on_rx)


M1_motor = PWM(Pin(4), freq=10000, duty=0)
M2_motor = PWM(Pin(5), freq=10000, duty=0)
M3_motor = PWM(Pin(40), freq=10000, duty=0)
M4_motor = PWM(Pin(41), freq=10000, duty=0)

try:
    while True:
        M1_motor.duty(value)
        M2_motor.duty(value)
        M3_motor.duty(value)
        M4_motor.duty(value)
        print("duty: ", value)
        time.sleep(3)

except KeyboardInterrupt:
    M1_motor.deinit()
    M2_motor.deinit()
    M3_motor.deinit()
    M4_motor.deinit()
    print("코드를 종료합니다.")

