class Box:
    def __init__(self, x1, y1 , x2 , y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def center_x(self):
        return (self.x1 + self.x2) / 2

    def center_y(self):
        return (self.y1 + self.y2) / 2

    @classmethod
    def from_center(cls, cx, cy, w, h):
        return cls(cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)

b1 = Box(500,400,700,600)
b2 = Box.from_center(600,500,200,200)

print(b1.center_x(), b2.center_x())
print(b2.x1, b2.y2)