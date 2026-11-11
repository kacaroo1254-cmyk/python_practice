import os
HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
from ultralytics import YOLO

# D30 의 구역 + D31 의 ID : ID 마다 구역 안에 머문 사진(프레임) 장수를 장부에 적습니다.

# ---- 내가 바꾸는 값 ----
VIDEO = "street.mp4"
CONF = 0.25
WANT = "person"
ZX1 = 300                               # 구역: 왼쪽 위 점
ZY1 = 300
ZX2 = 900                               # 구역: 오른쪽 아래 점
ZY2 = 700
STOP = 240                              # 사진(프레임)을 이 수만큼 보면 멈춘다 (240 = 영상 끝까지)
FPS = 24                                # 이 영상은 1초에 사진 약 24장
SHORT = 12                              # 구역 안에 이 장수보다 적게 있던 ID 는 따로 표시 (12장 = 약 0.5초)
from d31_video_output import make_video_path, get_video_fps, save_video_frame
OUTPUT_VIDEO = make_video_path("y9_dwell")
VIDEO_FPS = get_video_fps(VIDEO)
writer = None
model = YOLO("yolo26n.pt")
results = model.track(VIDEO, conf=CONF, stream=True, show=False, verbose=False)

stay = {}                               # ID 별 구역 안 프레임 수
frame = 0
count_sum = 0                           # 프레임별 인원 합
for result in results:
    frame = frame + 1
    inside_ids = []                     # 이번 프레임의 구역 안 ID
    for box in result.boxes:
        name = result.names[int(box.cls[0])]
        if name == WANT and box.id is not None:
            pid = int(box.id[0])        # 상자에 표시된 ID
            x1, y1, x2, y2 = box.xyxy[0]
            cx = (float(x1) + float(x2)) / 2
            cy = (float(y1) + float(y2)) / 2
            if ZX1 <= cx <= ZX2 and ZY1 <= cy <= ZY2:
                inside_ids.append(pid)
                count_sum = count_sum + 1
                if pid in stay:                     # 이미 본 ID
                    stay[pid] = stay[pid] + 1       # 프레임 수 +1
                else:                               # 처음 본 ID
                    stay[pid] = 1                   # 첫 프레임 기록
    writer = save_video_frame(writer, OUTPUT_VIDEO, result.plot(), VIDEO_FPS, zone=(ZX1, ZY1, ZX2, ZY2))
    print("프레임", frame, "번째: 구역 안 ID", inside_ids)
    if frame == STOP:                   # STOP 장을 봤으면
        break                           # 되풀이를 멈춘다

writer.release()
print("---- ID 별 구역 안 장수 (구역에 들어온 순서) ----")
short_ids = 0
for pid in stay:
    sec = round(stay[pid] / FPS, 1)     # 프레임 수를 초로 환산
    if stay[pid] < SHORT:
        short_ids = short_ids + 1
        print("ID", pid, ":", stay[pid], "장, 약", sec, "초  <- 짧다: ID 가 바뀐 조각일 수 있다")
    else:
        print("ID", pid, ":", stay[pid], "장, 약", sec, "초")

print("사진", frame, "장 / 구역에 들어온 서로 다른 ID", len(stay), "개 / 짧게 머문 ID", short_ids, "개")
print("프레임마다 센 구역 안 수를 모두 더하면", count_sum, "(같은 사람을 여러 번 센 수)")
print("동영상 저장:", OUTPUT_VIDEO)
