ZX1 = 300
ZX2 = 900
ZY1 = 300
ZY2 = 700

FPS = 24

def to_frames(sec):
    return sec * FPS

def is_inside(cx, cy):
    if ZX1 <= cx <= ZX2 and ZY1 <= cy <= ZY2:
        return True
    return False

print(is_inside(600, 500))
print(is_inside(100, 500))
print(is_inside(300, 500))

print(to_frames(2))



