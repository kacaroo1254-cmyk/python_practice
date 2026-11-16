def is_big(n):
    if n >= 100:
        return True
    return False

def is_inside(cx, cy):
    if 300 <= cx <= 900 and 300 <= cy <= 700:
        return True
    return False
print(is_inside(300, 300))      # True
print(is_inside(299, 500))      # False
print(is_inside(900, 701))      # False

print("---------------------------------------")

def is_left(cx):
    if cx <= 600:
        return True
    return False
print(is_left(900))
print(is_left(299))
print(is_left(500))