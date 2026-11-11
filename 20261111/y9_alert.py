import os
HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
from ultralytics import YOLO

# 머묾 경보: 구역 안에 LIMIT 장 넘게 머문 ID 에게 경보를 "한 번만" 냅니다.
# ID 가 없으면 사람이 구역 안에 있는 사진마다 경보가 되풀이됩니다.

# ---- 내가 바꾸는 값 ----
VIDEO = "street.mp4"
CONF = 0.25
WANT = "person"
ZX1 = 300                               # 구역: 왼쪽 위 점
ZY1 = 300
ZX2 = 900                               # 구역: 오른쪽 아래 점
ZY2 = 700
STOP = 240                              # 사진(프레임)을 이 수만큼 보면 멈춘다 (240 = 영상 끝까지)
LIMIT = 48                              # 구역 안에 이 장수가 되면 경보 (48장 = 약 2초)
from d31_video_output import make_video_path, get_video_fps, save_video_frame
OUTPUT_VIDEO = make_video_path("y9_alert")
VIDEO_FPS = get_video_fps(VIDEO)
writer = None
model = YOLO("yolo26n.pt")
results = model.track(VIDEO, conf=CONF, stream=True, show=False, verbose=False)

stay = {}                               # 장부: ID 번호 → 구역 안에 있던 사진 장수
alarms = 0                              # ID 로 낸 경보 수 (한 사람에 한 번)
frame_alarms = 0                        # ID 없이 냈다면: 구역 안에 사람이 있던 사진 수
frame = 0
for result in results:
    frame = frame + 1
    inside = 0
    for box in result.boxes:
        name = result.names[int(box.cls[0])]
        if name == WANT and box.id is not None:
            pid = int(box.id[0])
            x1, y1, x2, y2 = box.xyxy[0]
            cx = (float(x1) + float(x2)) / 2
            cy = (float(y1) + float(y2)) / 2
            if ZX1 <= cx <= ZX2 and ZY1 <= cy <= ZY2:
                inside = inside + 1
                if pid in stay:
                    stay[pid] = stay[pid] + 1
                else:
                    stay[pid] = 1
                if stay[pid] == LIMIT:              # 딱 LIMIT 장이 된 순간에만 (한 번)
                    alarms = alarms + 1
                    print("경보:", frame, "번째 사진, ID", pid, "가 구역 안에", LIMIT, "장 머묾")
    writer = save_video_frame(writer, OUTPUT_VIDEO, result.plot(), VIDEO_FPS, zone=(ZX1, ZY1, ZX2, ZY2))
    if inside > 0:
        frame_alarms = frame_alarms + 1
    if frame == STOP:                   # STOP 장을 봤으면
        break                           # 되풀이를 멈춘다

writer.release()
print("사진", frame, "장 / ID 로 낸 경보", alarms, "번 / ID 없이 사진마다 냈다면", frame_alarms, "번")
print("동영상 저장:", OUTPUT_VIDEO)
