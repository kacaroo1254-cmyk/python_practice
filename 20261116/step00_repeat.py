# step00_repeat.py

x1, x2 = 300, 900
center_x = (x1 + x2) / 2
print("x1: {}, x2: {}".format(x1, x2))
print("center_x: {}".format(center_x))

x1, x2 = 100, 300
center_x = (x1 + x2) / 2
print("x1: {}, x2: {}".format(x1, x2))
print("center_x: {}".format(center_x))

x1, x2 = 300, 900
center_x = (x1 + x2) / 2
print("x1: {}, x2: {}".format(x1, x2))
print("center_x: {}".format(center_x))

def make_center(x1, x2):
    center_x = (x1 + x2) / 2
    return center_x

def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    return x / y

result = add(1, 2)
print("result: {}".format(result))

def say_hello():
    print("----------")
    print("환영합니다")
    print("----------")

def show_area(w,h):
    result = w * h
    print("w: {}, h: {}, wh: {}".format(w, h, result))

show_area(4, 5)
show_area(10, 3)



