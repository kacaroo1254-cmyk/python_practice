# 클래스 생성
class Hello:
# 메소드 생성
    def greeting():
        print("Hello")

class HelloWorld:
    def greeting(self):
        print("Hello World")

# 인스턴스 생성
a = Hello()

# 메소드 호출
a.greeting()

a = HelloWorld()

a.greeting()
Hello().greeting()