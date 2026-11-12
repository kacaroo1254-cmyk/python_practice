
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

OUTPUT = "street_global_id.mp4"

# 객체가 사라진 것으로 판단하기까지 기다리는 프레임 수
MAX_MISSING_FRAMES = 90

# ------------------------------
# 2. 모델과 영상 준비
# ------------------------------

model = YOLO(WEIGHTS)

cap = cv2.VideoCapture(VIDEO)

if not cap.isOpened():
    raise RuntimeError("영상을 열 수 없습니다.")

fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

if fps <= 0:
    fps = 30.0

fourcc = cv2.VideoWriter_fourcc(*"mp4v")

writer = cv2.VideoWriter(
    OUTPUT, fourcc, fps, (width, height)
)

# ------------------------------
# 3. Global ID 관리 공간
# ------------------------------

active_tracks = {}

# YOLO ID : Global ID

last_seen = {}

# YOLO ID : 마지막으로 발견된 프레임

next_global_id = 100

# 지금까지 발급한 모든 Global ID
all_global_ids = set()

frame_count = 0

# ------------------------------
# 4. 영상 처리
# ------------------------------

while cap.isOpened():

    success, frame = cap.read()

    if not success:
        break

    frame_count += 1

    result = model.track(
        frame,
        persist=True,
        tracker="botsort.yaml",
        classes=[0],
        conf=CONF,
        verbose=False
    )[0]

    # --------------------------
    # 5. 오래 사라진 객체 정리
    # --------------------------

    expired_ids = []

    for track_id in list(active_tracks):

        missing_frames = frame_count - last_seen[track_id]

        if missing_frames > MAX_MISSING_FRAMES:
            expired_ids.append(track_id)

    for track_id in expired_ids:

        global_id = active_tracks.pop(track_id)
        last_seen.pop(track_id)

        print(
            f"추적 종료: Tracking ID {track_id} "
            f"/ Global ID {global_id}"
        )

    # --------------------------
    # 6. 현재 객체의 ID 확인
    # --------------------------

    if result.boxes.id is not None:

        track_ids = result.boxes.id.int().cpu().tolist()
        boxes = result.boxes.xyxy.int().cpu().tolist()

        for track_id, box in zip(track_ids, boxes):

            # 새로운 Tracking ID라면 Global ID 발급
            if track_id not in active_tracks:

                active_tracks[track_id] = next_global_id

                all_global_ids.add(next_global_id)

                print(
                    f"신규 발급: Tracking ID {track_id} "
                    f"-> Global ID {next_global_id}"
                )

                next_global_id += 1

            # 마지막 발견 프레임 갱신
            last_seen[track_id] = frame_count

            # Global ID 가져오기
            global_id = active_tracks[track_id]

            # 바운딩 박스 좌표
            x1, y1, x2, y2 = box

            # 사각형 그리기
            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2
            )

            # Global ID 표시
            cv2.putText(
                frame,
                f"Global ID: {global_id}",
                (x1, max(y1 - 10, 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )

    # --------------------------
    # 7. 현재 상태 화면 표시
    # --------------------------

    cv2.putText(
        frame,
        f"Unique IDs: {len(all_global_ids)}",
        (30, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 255),
        2
    )

    writer.write(frame)

    cv2.imshow("YOLO Global ID", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# ------------------------------
# 8. 최종 결과
# ------------------------------

print("\n========== Global ID 결과 ==========")

print("처리 프레임:", frame_count)

print("발급된 Global ID 개수:", len(all_global_ids))

print("Global ID 목록:", sorted(all_global_ids))

cap.release()
writer.release()
cv2.destroyAllWindows()

# 객체 자체의 정보를 저장하는 방식이 아닌 프레임의 정보를 저장하는 방식으로 같은사람에게서 다른 id가 여전히 나올 수 있음