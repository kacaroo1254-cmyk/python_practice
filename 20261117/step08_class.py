class Box:
    def __init__(self,x1,y1,x2,y2):
        print('__init__ 실행됨')
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def center_x(self):
        return (self.x1 + self.x2) / 2

    def center_y(self):
        return (self.y1 + self.y2) / 2

b1 = Box(500,400,700,600)

print(b1.center_x())
print(b1.center_y())