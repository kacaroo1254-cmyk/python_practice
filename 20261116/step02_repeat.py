def add(a,b):
    return a + b

answer = add(3,4)
print(answer)



FPS = 24

def to_frames(sec):
    a = sec * FPS
    b = 5
    return a, b

result = to_frames(2)
print(result)

def calculate(x, y):
    return x + y, x - y, x * y, x / y

a, b, c, d = calculate(6, 2)

print("x + y: {},\n"
      "x - y: {},\n"
      "x * y: {},\n"
      "x / y: {}"
      .format(a, b, c, d))


