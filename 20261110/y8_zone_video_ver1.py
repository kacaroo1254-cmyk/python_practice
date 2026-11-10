import os
import cv2
from ultralytics import YOLO

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)

# ---- 내가 바꾸는 값 ----
VIDEO = "street.mp4"
CONF = 0.25
WANT = "person"

ZX1 = 300                 # 구역 왼쪽 위 X
ZY1 = 300                 # 구역 왼쪽 위 Y
ZX2 = 900                 # 구역 오른쪽 아래 X
ZY2 = 700                 # 구역 오른쪽 아래 Y

ALERT = 5                 # 구역 안 인원이 이 수 이상이면 경고

OUTPUT = "street_zone.mp4"

# ---- YOLO 모델 준비 ----
model = YOLO("yolo26n.pt")

# 영상 정보 가져오기
cap = cv2.VideoCapture(VIDEO)

fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# 영상 저장 도구 준비
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
writer = cv2.VideoWriter(
    OUTPUT,
    fourcc,
    fps,
    (width, height)
)

cap.release()

# ---- YOLO 객체 검출 ----
results = model(
    VIDEO,
    conf=CONF,
    stream=True,
    verbose=False
)

frame = 0
alerts = 0
most = 0

for result in results:

    # YOLO 검출 결과를 이미지로 변환
    img = result.plot(labels=False)

    inside = 0

    # 검출된 객체 하나씩 확인
    for box in result.boxes:

        name = result.names[int(box.cls[0])]

        if name == WANT:

            x1, y1, x2, y2 = box.xyxy[0]

            cx = (float(x1) + float(x2)) / 2
            cy = (float(y1) + float(y2)) / 2

            # 객체 중심점이 지정 구역 안에 있는지 확인
            if ZX1 <= cx <= ZX2 and ZY1 <= cy <= ZY2:
                inside += 1

    # 경고 횟수 계산
    if inside >= ALERT:
        alerts += 1

    # 구역 안 최대 인원 갱신
    if inside > most:
        most = inside

    frame += 1

    # 감지 구역 사각형 그리기
    cv2.rectangle(
        img,
        (ZX1, ZY1),
        (ZX2, ZY2),
        (0, 255, 255),
        10
    )

    # 현재 구역 안 인원 표시
    cv2.putText(
        img,
        f"Person: {inside}",
        (ZX1, ZY1 - 20),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 255),
        2
    )

    # 경고 표시
    if inside >= ALERT:
        cv2.putText(
            img,
            "WARNING!",
            (50, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            2,
            (0, 0, 255),
            4
        )

    # 수정된 프레임을 영상에 추가
    writer.write(img)

# 영상 파일 닫기
writer.release()

# 결과 출력
print("사진", frame, "장 중 경고", alerts,
      "장, 구역 안 최대", most, "명")

print("저장 완료:", OUTPUT)
