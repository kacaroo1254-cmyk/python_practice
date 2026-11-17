class Box:
    def __init__(self,x1,x2):
        print("__init__ 실행됨")
        self.x1 = x1
        self.x2 = x2

b1 = Box(500,400)
b2 = Box(0,200)


print(b1.x1)
print(b2.x1)