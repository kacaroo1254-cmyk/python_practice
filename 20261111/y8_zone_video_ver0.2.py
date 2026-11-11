
import os
from pathlib import Path
from ultralytics import YOLO
import cv2


# ---- 현재 파이썬 파일 위치 설정 ----
HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)


# ---- 내가 바꾸는 값 ----
VIDEO = "street.mp4"
CONF = 0.25
WANT = "person"

ZX1 = 300                         # 구역 왼쪽 위 X
ZY1 = 300                         # 구역 왼쪽 위 Y
ZX2 = 900                         # 구역 오른쪽 아래 X
ZY2 = 700                         # 구역 오른쪽 아래 Y

ALERT = 5                         # 경고 기준 인원


# ---- 저장 위치 설정 ----
SAVE_DIR = Path("C:/sjs/python/pjt/20261111/street_result")
SAVE_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT = str(SAVE_DIR / "street_result.mp4")


# ---- 원본 영상 정보 가져오기 ----
cap = cv2.VideoCapture(VIDEO)

fps = cap.get(cv2.CAP_PROP_FPS)

if fps <= 0:
    fps = 30

cap.release()


# ---- YOLO 모델 실행 ----
model = YOLO("yolo26n.pt")

results = model(
    VIDEO,
    conf=CONF,
    stream=True,
    verbose=False,
    save=False
)


# ---- 영상 저장 준비 ----
writer = None

frame = 0
alerts = 0
most = 0


try:
    for result in results:

        # YOLO 탐지 결과를 이미지로 가져오기
        img = result.plot(labels=False)

        # 현재 이미지 크기 가져오기
        height, width = img.shape[:2]

        # 첫 번째 프레임에서 영상 저장기 생성
        if writer is None:

            fourcc = cv2.VideoWriter_fourcc(*"mp4v")

            writer = cv2.VideoWriter(
                OUTPUT,
                fourcc,
                fps,
                (width, height)
            )

            if not writer.isOpened():
                raise RuntimeError("영상 저장기를 열 수 없습니다.")

        # 구역 사각형 그리기
        cv2.rectangle(
            img,
            (ZX1, ZY1),
            (ZX2, ZY2),
            (0, 255, 255),
            10
        )

        inside = 0

        # 탐지된 객체 하나씩 확인
        for box in result.boxes:

            name = result.names[int(box.cls[0])]

            # 사람만 확인
            if name == WANT:

                x1, y1, x2, y2 = box.xyxy[0]

                # 사람의 중심 좌표 계산
                cx = (float(x1) + float(x2)) / 2
                cy = (float(y1) + float(y2)) / 2

                # 중심 좌표가 구역 안에 있는지 확인
                if ZX1 <= cx <= ZX2 and ZY1 <= cy <= ZY2:
                    inside += 1

        # 경고 기준 확인
        if inside >= ALERT:
            alerts += 1

            # 경고 문구 표시
            cv2.putText(
                img,
                "WARNING!",
                (ZX1, ZY1 - 20),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.5,
                (0, 0, 255),
                3,
                cv2.LINE_AA
            )

        # 최대 인원 갱신
        if inside > most:
            most = inside

        # 현재 구역 인원 표시
        cv2.putText(
            img,
            f"People: {inside}",
            (ZX1, ZY2 + 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.0,
            (0, 255, 255),
            2,
            cv2.LINE_AA
        )

        # 수정된 이미지를 영상에 추가
        writer.write(img)

        frame += 1

finally:
    # 영상 저장 종료
    if writer is not None:
        writer.release()


# ---- 최종 결과 출력 ----
print("분석 프레임:", frame)
print("경고 프레임:", alerts)
print("구역 안 최대 인원:", most)
print("저장 위치:", OUTPUT)
