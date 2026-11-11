import os
from ultralytics import YOLO

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)

# ---- 내가 바꾸는 값 ----
VIDEO = "street.mp4"
CONF = 0.25
WANT = "person"
ZX1 = 300                               # 구역: 왼쪽 위 점
ZY1 = 300
ZX2 = 900                               # 구역: 오른쪽 아래 점
ZY2 = 700
ALERT = 5                               # 구역 안이 이 수 이상이면 경고

model = YOLO("yolo26n.pt")
results = model(VIDEO,
                conf=CONF,
                stream=True,
                verbose=False,
                save=True,
                name="zone_결과")



frame = 0
alerts = 0                              # 경고가 난 사진(프레임)의 수
most = 0                                # 구역 안에서 가장 많았던 수
for result in results:
    inside = 0
    for box in result.boxes:
        name = result.names[int(box.cls[0])]
        if name == WANT:
            x1, y1, x2, y2 = box.xyxy[0]
            cx = (float(x1) + float(x2)) / 2
            cy = (float(y1) + float(y2)) / 2
            if ZX1 <= cx <= ZX2 and ZY1 <= cy <= ZY2:
                inside = inside + 1
    if inside >= ALERT:
        alerts = alerts + 1
    if inside > most:
        most = inside
    frame = frame + 1

print("사진", frame, "장 중 경고", alerts, "장, 구역 안 최대", most, "명")
