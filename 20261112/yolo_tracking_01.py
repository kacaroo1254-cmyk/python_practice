
import os
import cv2
from ultralytics import YOLO

# ------------------------------
# 1. 기본 설정
# ------------------------------

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)

VIDEO = "street.mp4"
WEIGHTS = "yolo26n.pt"
CONF = 0.25

OUTPUT = "street_tracking.mp4"

# ------------------------------
# 2. YOLO 모델 및 영상 불러오기
# ------------------------------

model = YOLO(WEIGHTS)

cap = cv2.VideoCapture(VIDEO)

if not cap.isOpened():
    raise RuntimeError("영상을 열 수 없습니다.")

# 영상 정보 가져오기
fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

if fps <= 0:
    fps = 30.0

# 결과 영상 저장 준비
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
writer = cv2.VideoWriter(
    OUTPUT, fourcc, fps, (width, height)
)

# ------------------------------
# 3. Tracking ID 저장 공간
# ------------------------------

seen_ids = set()

frame_count = 0

# ------------------------------
# 4. 영상 프레임 반복 처리
# ------------------------------

while cap.isOpened():

    success, frame = cap.read()

    if not success:
        break

    frame_count += 1

    # 사람 추적 실행
    result = model.track(
        frame,
        persist=True,
        tracker="botsort.yaml",
        classes=[0],
        conf=CONF,
        verbose=False
    )[0]

    # 현재 프레임의 Tracking ID 가져오기
    if result.boxes.id is not None:

        track_ids = result.boxes.id.int().cpu().tolist()

        for track_id in track_ids:

            # 기존에 없던 ID라면 저장
            if track_id not in seen_ids:
                seen_ids.add(track_id)

                print("새로운 Tracking ID:", track_id)

    # 감지 결과에 바운딩 박스와 ID 표시
    annotated_frame = result.plot()

    # 현재까지 등장한 고유 ID 개수 표시
    cv2.putText(
        annotated_frame,
        f"Unique IDs: {len(seen_ids)}",
        (30, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    # 결과 영상 저장
    writer.write(annotated_frame)

    # 화면 출력
    cv2.imshow("YOLO Tracking", annotated_frame)

    # Q를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# ------------------------------
# 5. 결과 출력 및 자원 정리
# ------------------------------

print("\n========== Tracking 결과 ==========")
print("처리한 프레임:", frame_count)
print("고유 Tracking ID 개수:", len(seen_ids))
print("ID 목록:", sorted(seen_ids))

cap.release()
writer.release()
cv2.destroyAllWindows()

# 단순 id가 중복생성되는것을 막아주는방법
# 같은사람에게서 여전히 다른 id가 나올 수 있음
# 하지만 다른사람끼리는 같은 id가 나올 수 없음