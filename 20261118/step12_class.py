class Box:
    def __init__(self, x1 = 0, y1 = 0, x2 = 0, y2 = 0):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def center_x(self):
        return (self.x1 + self.x2) / 2

b0 = Box()
b1 = Box(500)
b2 = Box(x2 = 500)

print(b0.center_x())
print(b1.center_x())
print(b2.center_x())