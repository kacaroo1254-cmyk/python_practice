from machine import Pin
import time

flash = Pin(4, Pin.OUT, value= 0)
red = Pin(33, Pin.OUT, value= 1)

def blink_red():
    red.value(0)

def blink_flash():
    flash.value(1)

i = 108
try:
    while True:
        time.sleep_ms(735)
        blink_red()
        print (i)
        if i < 10:
            if i % 3 == 0:
                blink_flash()
                print('짝!')
        elif i < 100:
            first_num = int(i/10)
            second_num = i % 10
            if first_num % 3 == 0:
                blink_flash()
                print('짝!')
            if second_num % 3 == 0 and second_num!= 0:
                blink_flash()
                print('짝!')
        else:
            first_num = int(i/100)
            second_num = int((i - (first_num * 100)) / 10)
            third_num = (i - (first_num * 100)) % 10
            if first_num % 3 == 0:
                blink_flash()
                print('짝!')
            if second_num % 3 == 0 and second_num!= 0:
                blink_flash()
                print('짝!')
            if third_num % 3 == 0 and third_num!= 0:
                blink_flash()
                print('짝!')
                
        i += 1
        time.sleep_ms(250)
        red.value(1)
        flash.value(0)
        

finally:
    flash.value(0)
    red.value(1)

# 110에서 박수를 침 120번대에서도 박수침-해결완
