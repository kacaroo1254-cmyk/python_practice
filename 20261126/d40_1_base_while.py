import os
import cv2
from ultralytics import YOLO

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
NUMBER = 1
PHOTO_DIR = "test_images"
MAKERESULT_DIR = "results_mine"
if not os.path.isdir(PHOTO_DIR):
    raise FileNotFoundError("test_images 폴더가 없습니다.")
photo_names = sorted(name for name in os.listdir(PHOTO_DIR)
                     if name.lower().endswith((".jpg", ".jpeg", ".png")))
if not photo_names:
    raise FileNotFoundError("test_images 폴더에 JPG, JPEG, PNG 사진이 없습니다.")
if not 1 <= NUMBER <= len(photo_names):
    raise ValueError(f"NUMBER는 1부터 {len(photo_names)} 사이여야 합니다.")
while NUMBER<=len(photo_names):
    PHOTO = os.path.join(PHOTO_DIR, photo_names[NUMBER - 1])
    WEIGHT = "my_cat_best.pt"
    model = YOLO(WEIGHT)
    result = model.predict(PHOTO, conf=0.25, verbose=False)[0]
    print("사진 번호:", NUMBER, "/", len(photo_names), photo_names[NUMBER - 1])
    for box in result.boxes:
        print(model.names[int(box.cls)], f"점수 {float(box.conf):.2f}")
    os.makedirs(MAKERESULT_DIR, exist_ok=True)
    prefix = "base" if WEIGHT == "yolo26n.pt" else "mine"
    output = os.path.join(MAKERESULT_DIR, f"{prefix}_{NUMBER}.jpg")
    if not cv2.imwrite(output, result.plot()):
        raise OSError("결과 그림을 저장하지 못했습니다: " + output)
    NUMBER += 1
    print("저장:", output)
