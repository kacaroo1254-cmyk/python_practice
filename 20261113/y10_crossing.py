import os
import cv2
from ultralytics import YOLO
from d31_video_output import make_video_path, get_video_fps, save_video_frame

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)

# ---- 내가 바꾸는 값 ----
VIDEO = "street.mp4"
CONF = 0.25
WANT = "person"
LINE_X = 640                         # 화면을 A와 B로 나누는 세로선
STOP = 240                           # 이 영상의 전체 프레임 수
OUTPUT_VIDEO = make_video_path("y10_crossing")
VIDEO_FPS = get_video_fps(VIDEO)
writer = None
model = YOLO("yolo26n.pt")
results = model.track(VIDEO, conf=CONF, stream=True, show=False, verbose=False)

previous_side = {}                   # ID 번호마다 직전 위치(A 또는 B)
in_count = 0                         # A에서 B로 간 통과 후보 수
out_count = 0                        # B에서 A로 간 통과 후보 수
frame = 0
inside_ids = []                      # 마지막 요약에서 쓰려고 미리 만들어 둠

for result in results:
    frame = frame + 1
    inside_ids = []
    events = []
    for box in result.boxes:
        name = result.names[int(box.cls[0])]
        if name == WANT and box.id is not None:
            pid = int(box.id[0])                                  # 이 상자의 추적 ID 번호
            x1, y1, x2, y2 = box.xyxy[0]                          # 상자의 왼쪽·위·오른쪽·아래 좌표
            center_x = (float(x1) + float(x2)) / 2                # 왼쪽 끝과 오른쪽 끝의 한가운데 x
            if center_x < LINE_X:                                 # 640보다 작으면 A, 아니면(640 포함) B
                side = "A"
            else:
                side = "B"
            if side == "B":                                       # B쪽이면 현재 B쪽 ID 목록에 넣음
                inside_ids.append(pid)
            if pid in previous_side:                              # 직전 위치가 기억된 ID만 비교(처음 본 ID는 건너뜀)
                if previous_side[pid] == "A" and side == "B":     # 직전 A, 지금 B
                    in_count = in_count + 1
                    events.append((pid, "A→B 입장 후보"))
                elif previous_side[pid] == "B" and side == "A":   # 직전 B, 지금 A
                    out_count = out_count + 1
                    events.append((pid, "B→A 퇴장 후보"))
            previous_side[pid] = side                             # 비교가 끝난 뒤 지금 위치를 기억
    inside_ids.sort()
    for pid, direction in events:
        print("통과 후보:", frame, "번째 프레임, ID", pid, direction)
    print("프레임", frame, "번째: 현재 B쪽 ID", inside_ids)
    img = result.plot()
    height = img.shape[0]
    cv2.line(img, (LINE_X, 0), (LINE_X, height), (0, 255, 255), 3)
    writer = save_video_frame(writer, OUTPUT_VIDEO, img, VIDEO_FPS)
    if frame == STOP:
        break

writer.release()
print("---- 방향별 통과 후보 ----")
print("A→B 입장 후보", in_count, "건 / B→A 퇴장 후보", out_count, "건")
print("마지막 프레임 B쪽 현재 추적 ID", inside_ids, "/", len(inside_ids), "개")
print("사진", frame, "장 / ID는 실제 신원을 보증하지 않음")
print("동영상 저장:", OUTPUT_VIDEO)
