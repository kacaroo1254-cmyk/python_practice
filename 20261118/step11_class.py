ZX1 = 100
ZY1 = 500
ZX2 = 600
ZY2 = 700


def is_inside(cx, cy):
    if ZX1 <= cx <= ZX2 and ZY1 <= cy <= ZY2:
        return True
    return False

class Box:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def center_x(self):
        return (self.x1 + self.x2) / 2

    def center_y(self):
        return (self.y1 + self.y2) / 2

    def in_zone(self):
        cx = self.center_x()
        cy = self.center_y()
        return is_inside(cx, cy)

b1 = Box(500, 400, 700, 600)
b2 = Box(0, 400, 200, 600)

print(b1.in_zone())
print(b2.in_zone())