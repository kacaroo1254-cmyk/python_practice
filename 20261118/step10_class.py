class Box:
    def __init__(self, x1, x2):
        self.x1 = x1
        self.x2 = x2
    def center_x(self):
        return (self.x1 + self.x2) / 2

b = Box(500, 700)

print(b.center_x())