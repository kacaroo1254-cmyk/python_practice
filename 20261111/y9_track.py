import os
from ultralytics import YOLO

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)

# ---- 내가 바꾸는 값 ----
VIDEO = "street.mp4"
CONF = 0.25
WANT = "person"

from d31_video_output import make_video_path, get_video_fps, save_video_frame

OUTPUT_VIDEO = make_video_path("y9_track")
VIDEO_FPS = get_video_fps(VIDEO)
writer = None
model = YOLO("yolo26n.pt")
results = model.track(VIDEO, conf=CONF,
                      stream=True, verbose=False)

frame = 0
all_ids = []                # 지금까지 나온 번호
for result in results:
    ids = []                # 이 프레임의 번호
    for box in result.boxes:
        name = result.names[int(box.cls[0])]
        if name == WANT:
            if box.id is not None:
                num = int(box.id[0])
                ids.append(num)
                if num not in all_ids:
                    all_ids.append(num)
    ids.sort()
    writer = save_video_frame(writer, OUTPUT_VIDEO, result.plot(), VIDEO_FPS)
    frame = frame + 1
    print("프레임", frame, "번째: 사람 ID", ids)

writer.release()
print("전체", frame, "프레임 / 서로 다른 사람 ID", len(all_ids), "개")
print("동영상 저장:", OUTPUT_VIDEO)
