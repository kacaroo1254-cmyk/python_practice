import os
import cv2
from ultralytics import YOLO

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
NUMBER = 1
PHOTO_DIR = "test_images"
if not os.path.isdir(PHOTO_DIR):
    raise FileNotFoundError("test_images 폴더가 없습니다.")
photo_names = sorted(name for name in os.listdir(PHOTO_DIR)
                     if name.lower().endswith((".jpg", ".jpeg", ".png")))
if not photo_names:
    raise FileNotFoundError("test_images 폴더에 JPG, JPEG, PNG 사진이 없습니다.")
if not 1 <= NUMBER <= len(photo_names):
    raise ValueError(f"NUMBER는 1부터 {len(photo_names)} 사이여야 합니다.")
PHOTO = os.path.join(PHOTO_DIR, photo_names[NUMBER - 1])
models = [("base", YOLO("yolo26n.pt")), ("mine", YOLO("best.pt"))]
os.makedirs("results", exist_ok=True)
print("사진 번호:", NUMBER, "/", len(photo_names), photo_names[NUMBER - 1])
for label, model in models:
    saved_result = None
    for threshold in (0.25, 0.5):
        result = model.predict(PHOTO, conf=threshold, verbose=False)[0]
        print(label, f"conf={threshold:.2f}", "찾은 개수:", len(result.boxes))
        for box in result.boxes:
            name = model.names[int(box.cls)]
            print(" ", name, f"점수 {float(box.conf):.2f}")
        if threshold == 0.25:
            saved_result = result
    output = os.path.join("results", f"{label}_{NUMBER}.jpg")
    if not cv2.imwrite(output, saved_result.plot()):
        raise OSError("결과 그림을 저장하지 못했습니다: " + output)
    print("저장:", output)
