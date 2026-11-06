from ultralytics import YOLO

model = YOLO("yolo26n.pt")              # 가장 작은 YOLO 파일을 불러와 model 이라는 이름을 붙인다

print("YOLO 가 아는 이름 :", len(model.names), "가지")     # model.names : 번호와 이름을 모아 둔 목록
for number in model.names:              # 목록의 번호를 하나씩 꺼낸다
    print(number, model.names[number])  # 번호와 그 번호의 이름을 한 줄씩 쓴다
