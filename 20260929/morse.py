from machine import Pin
import time

flash = Pin(4, Pin.OUT, value=0)

morse = {
    'A': [1, 3],
    'B': [3, 1, 1, 1],
    'C': [3, 1, 3, 1],
    'D': [3, 1, 1],
    'E': [1],
    'F': [1, 1, 3, 1],
    'G': [3, 3, 1],
    'H': [1, 1, 1, 1],
    'I': [1, 1],
    'J': [1, 3, 3, 3],
    'K': [3, 1, 3],
    'L': [1, 3, 1, 1],
    'M': [3, 3],
    'N': [3, 1],
    'O': [3, 3, 3],
    'P': [1, 3, 3, 1],
    'Q': [3, 3, 1, 3],
    'R': [1, 3, 1],
    'S': [1, 1, 1],
    'T': [3],
    'U': [1, 1, 3],
    'V': [1, 1, 1, 3],
    'W': [1, 3, 3],
    'X': [3, 1, 1, 3],
    'Y': [3, 1, 3, 3],
    'Z': [3, 3, 1, 1]
}

UNIT = 150

def blink_morse(i):
    flash.value(1)
    time.sleep_ms(i * UNIT)
    flash.value(0)
    time.sleep_ms(300)
    
word = input("단어를 입력하세요:").upper()
    
for s in word:
    for  i in morse[s]:
        blink_morse(i)
        
    time.sleep_ms(600)
        
        
