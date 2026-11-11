import os
import cv2
from ultralytics import YOLO

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)

# ---- 조각 1 : 값 모음 (y8 에서 가져옴) ----
VIDEO = "street.mp4"
CONF = 0.25
WANT = "person"
ZX1 = 300                               # 구역: 왼쪽 위 점
ZY1 = 300
ZX2 = 900                               # 구역: 오른쪽 아래 점
ZY2 = 700
ALERT = 5                               # 구역 안이 이 수 이상이면 경고
from d31_video_output import make_video_path, get_video_fps, save_video_frame
OUTPUT_VIDEO = make_video_path("y8b_zone_box_video")
VIDEO_FPS = get_video_fps(VIDEO)
writer = None
model = YOLO("yolo26n.pt")
results = model(VIDEO, conf=CONF, stream=True, verbose=False)

frame = 0
alerts = 0
most = 0
for result in results:
    # ---- 조각 2 : 구역 안 사람 세기 (y8 에서 가져옴) ----
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

    # ---- 조각 3 : 구역을 그려 넣기 (y7 에서 가져옴) ----
    img = result.plot(labels=False)
    cv2.rectangle(img, (ZX1, ZY1), (ZX2, ZY2), (0, 255, 255), 4)

    # ---- 조각 4 : 구역 안 사람 수를 글자로 쓰기 (글자 준비 + putText) ----
    text = "inside " + str(inside)
    cv2.putText(img, text, (ZX1, ZY1 - 15),
                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 255), 3)

    # ---- 조각 5 : 창에 보이기 ----
    writer = save_video_frame(writer, OUTPUT_VIDEO, img, VIDEO_FPS)
    cv2.imshow("zone", img)
    cv2.waitKey(1)

    print("프레임", frame, "번째: 구역 안", inside, "명")

writer.release()
print("프레임", frame, "장 중 경고", alerts, "장, 구역 안 최대", most, "명")
print("동영상 저장:", OUTPUT_VIDEO)
cv2.destroyAllWindows()
