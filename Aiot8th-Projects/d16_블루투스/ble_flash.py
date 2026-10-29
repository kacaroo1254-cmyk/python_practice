from machine import Pin, PWM, Timer
import bluetooth,ble_simple_peripheral,time

ble = bluetooth.BLE()
p = ble_simple_peripheral.BLESimplePeripheral(ble,name='pyD_2344')
value = ''

def on_rx(read):
    global value
    print("RX", read)
    value = read
    return value
    
    
p.on_write(on_rx)


M1_motor = PWM(Pin(4), freq=10000, duty=0)
M2_motor = PWM(Pin(5), freq=10000, duty=0)
M3_motor = PWM(Pin(40), freq=10000, duty=0)
M4_motor = PWM(Pin(41), freq=10000, duty=0)

try:
    while True:
        M1_motor.duty(0)
        M2_motor.duty(0)
        M3_motor.duty(0)
        M4_motor.duty(0)
        print("duty: ", 0)
        time.sleep(3)

except KeyboardInterrupt:
    M1_motor.deinit()
    M2_motor.deinit()
    M3_motor.deinit()
    M4_motor.deinit()
    print("코드를 종료합니다.")
