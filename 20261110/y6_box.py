import os                               # 폴더·파일 이름을 다루는 도구 상자(os)를 가져온다
from ultralytics import YOLO            # ultralytics 도구 상자에서 YOLO 하나만 꺼낸다

HERE = os.path.dirname(os.path.abspath(__file__))   # 이 파일이 들어 있는 폴더의 전체 주소 (예: my_drone8/d29_photo)
os.chdir(HERE)                          # 파이썬의 작업 위치를 이 폴더로 옮긴다 (결과·모델이 이 폴더에 생기게 한다)

# ---- 내가 바꾸는 값 ----
PHOTO = "street.jpg"                    # 같은 폴더에 있는 사진 이름 (따옴표 안에 쓴다)
CONF = 0.25                             # 자신감 기준 : 자신감이 이 숫자보다 낮은 네모는 버린다 (0 ~ 1 사이)
WANT = "person"                         # 찾고 싶은 이름 (따옴표 안에 쓴다)

model = YOLO("yolo26n.pt")              # 가장 작은 YOLO 파일을 불러와 model 이라는 이름을 붙인다
results = model(PHOTO, conf=CONF, verbose=False)   # 사진을 보여 준다 (자신감 기준 적용, 자동 출력 줄은 끈다)
result = results[0]                     # 답 묶음의 0번째 = 사진 한 장에 대한 답

count = 0                               # 센 사람 수 : 처음에는 0
for box in result.boxes:                # 찾은 네모를 하나씩 꺼낸다
    name = result.names[int(box.cls[0])]        # 이름 번호(정수)를 이름 글자로 바꾼다
    if name == WANT:                    # 찾고 싶은 이름이면
        conf = round(float(box.conf[0]), 2)     # 자신감을 소수 둘째 자리까지 줄인다
        x1, y1, x2, y2 = box.xyxy[0]    # 네모의 위치 숫자 4개를 한 번에 네 이름으로 받는다 (왼쪽 위 점 x1 y1, 오른쪽 아래 점 x2 y2)
        x1 = int(x1)                    # 소수를 정수로 바꾼다 (사진 칸 번호는 정수)
        y1 = int(y1)                    # 소수를 정수로 바꾼다
        x2 = int(x2)                    # 소수를 정수로 바꾼다
        y2 = int(y2)                    # 소수를 정수로 바꾼다
        print(name, conf, x1, y1, x2, y2)       # 이름 자신감 x1 y1 x2 y2 를 한 줄로 쓴다
        count = count + 1               # 센 수에 1 을 더해 다시 count 에 넣는다

print(PHOTO, "에서", WANT, "는", count, "개")     # 사진 이름, 찾은 이름, 센 개수를 한 줄로 쓴다
result.save("y6_box.jpg")               # 네모를 그린 사진을 파일로 저장한다 (이 폴더에 생긴다)
