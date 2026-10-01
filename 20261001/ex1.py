"""GPIO 4의 flash LED를 사용한다.
Flash LED를 0.5초 ON → 0.5초 OFF 한다.
이 동작을 반복할 때마다 counter를 1씩 증가시킨다.
counter가 3이 되면
빨간 LED(GPIO 33)를 ON 한다.
counter를 다시 0으로 만든다.
프로그램은 Ctrl+C로 중단할 수 있도록 try ... finally를 사용한다.
프로그램이 종료되면:
Flash LED → OFF
빨간 LED → OFF
빨간 LED는 네 ESP32-CAM에서 Active-Low이므로:
red.value(0) → ON
red.value(1) → OFF"""

from machine import Pin
import time

flash_led = Pin(4, Pin.OUT, value=0)
red_led = Pin(33, Pin.OUT, value=1)

counter = 1

try:
    while True:
        flash_led.value(1)
        if counter == 3:
            red_led.value(0)
        time.sleep_ms(500)
        flash_led.value(0)
        if counter == 3:
            red_led.value(1)
            counter = 0
        time.sleep_ms(500)
        counter += 1
    
    
finally:
    flash_led.value(0)
    red_led.value(1)