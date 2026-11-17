# error_self_missing.py
class Box:
    def __init__(self, x1, x2):
        self.x1 = x1
        self.x2 = x2
    def center_x(self):
        return (self.x1 + self.x2) / 2
b1 = Box(500, 700)
print(b1.center_x())

# q2_3_argument.py
# 문제: Run 뒤 오류를 읽고 Box(500)에 빠진 값을 추가해 600.0을 출력하세요.
class Box1:
    def __init__(self, x1, x2):
        self.x1 = x1
        self.x2 = x2
b2 = Box1(500, 600)
print((b2.x1 + b2.x2) / 2)