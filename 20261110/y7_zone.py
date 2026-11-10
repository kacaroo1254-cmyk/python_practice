import os                               # 폴더·파일 이름을 다루는 도구 상자(os)를 가져온다
from ultralytics import YOLO            # ultralytics 도구 상자에서 YOLO 하나만 꺼낸다

HERE = os.path.dirname(os.path.abspath(__file__))   # 이 파일이 들어 있는 폴더의 전체 주소
os.chdir(HERE)                          # 파이썬의 작업 위치를 이 폴더로 옮긴다 (결과·모델이 이 폴더에 생기게 한다)

# ---- 내가 바꾸는 값 ----
PHOTO = "street.jpg"                    # 같은 폴더에 있는 사진 이름 (따옴표 안에 쓴다)
CONF = 0.25                             # 자신감 기준 (0 ~ 1 사이)
WANT = "person"                         # 찾고 싶은 이름 (따옴표 안에 쓴다)
ZX1 = 600                               # 구역의 왼쪽 위 점 : 가로 위치
ZY1 = 800                               # 구역의 왼쪽 위 점 : 세로 위치
ZX2 = 1000                              # 구역의 오른쪽 아래 점 : 가로 위치
ZY2 = 1280                              # 구역의 오른쪽 아래 점 : 세로 위치

model = YOLO("yolo26n.pt")              # 가장 작은 YOLO 파일을 불러와 model 이라는 이름을 붙인다
results = model(PHOTO, conf=CONF, verbose=False)   # 사진을 보여 준다
result = results[0]                     # 답 묶음의 0번째 = 사진 한 장에 대한 답

total = 0                               # 센 사람 수 : 처음에는 0
inside = 0                              # 구역 안에 있는 사람 수 : 처음에는 0
for box in result.boxes:                # 찾은 네모를 하나씩 꺼낸다
    name = result.names[int(box.cls[0])]        # 이름 번호(정수)를 이름 글자로 바꾼다
    if name == WANT:                    # 찾고 싶은 이름이면
        x1, y1, x2, y2 = box.xyxy[0]    # 네모의 위치 숫자 4개를 받는다
        cx = (float(x1) + float(x2)) / 2        # 가운데 점의 가로 위치 : 왼쪽과 오른쪽을 더해 2 로 나눈다
        cy = (float(y1) + float(y2)) / 2        # 가운데 점의 세로 위치 : 위쪽과 아래쪽을 더해 2 로 나눈다
        total = total + 1               # 센 수에 1 을 더한다
        if ZX1 <= cx <= ZX2 and ZY1 <= cy <= ZY2:       # 가로도 구역 안이고, 세로도 구역 안이면
            inside = inside + 1         # 구역 안 수에 1 을 더한다
            print(total, "번 사람 : 가운데", round(cx), round(cy), "→ 구역 안")
        else:                           # 그렇지 않으면
            print(total, "번 사람 : 가운데", round(cx), round(cy), "→ 구역 밖")

print(PHOTO, "에서", WANT, "는", total, "명, 구역 안은", inside, "명")      # 전체 수와 구역 안 수를 한 줄로 쓴다

import cv2                              # 사진에 선을 그리는 도구 상자(cv2)를 가져온다
img = result.plot(labels=False)         # 네모만 그려진 사진을 꺼낸다 (이름 글자는 뺀다)
cv2.rectangle(img, (ZX1, ZY1), (ZX2, ZY2), (0, 255, 255), 10)   # 구역을 노란 네모로 그려 넣는다 (노랑, 두께 10)
cv2.imwrite("y7_zone.jpg", img)         # 그린 사진을 파일로 저장한다 (이 폴더에 생긴다)
