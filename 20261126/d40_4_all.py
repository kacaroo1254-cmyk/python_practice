import os
import cv2
from ultralytics import YOLO

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
PHOTO_DIR = "test_images"
if not os.path.isdir(PHOTO_DIR):
    raise FileNotFoundError("test_images 폴더가 없습니다.")
photo_names = sorted(name for name in os.listdir(PHOTO_DIR)
                     if name.lower().endswith((".jpg", ".jpeg", ".png")))
if not photo_names:
    raise FileNotFoundError("test_images 폴더에 JPG, JPEG, PNG 사진이 없습니다.")
models = [("base", YOLO("yolo26n.pt")), ("mine", YOLO("best.pt"))]
run_number = 1
while os.path.exists(os.path.join("results", f"run_{run_number:02d}")):
    run_number += 1
run_dir = os.path.join("results", f"run_{run_number:02d}")
os.makedirs(run_dir)
found = {"base": 0, "mine": 0}
for NUMBER, photo_name in enumerate(photo_names, start=1):
    if not 1 <= NUMBER <= len(photo_names):
        raise ValueError(f"NUMBER는 1부터 {len(photo_names)} 사이여야 합니다.")
    photo = os.path.join(PHOTO_DIR, photo_name)
    print(f"{NUMBER:02d}/{len(photo_names):02d}", photo_name, end=" | ")
    for label, model in models:
        result = model.predict(photo, conf=0.25, verbose=False)[0]
        scores = [float(box.conf) for box in result.boxes]
        found[label] += bool(scores)
        output = os.path.join(run_dir, f"{label}_{NUMBER:02d}.jpg")
        if not cv2.imwrite(output, result.plot()):
            raise OSError("결과 그림을 저장하지 못했습니다: " + output)
        print(f"{label} {len(scores)}개 최고 {max(scores, default=0):.2f}", end=" | ")
    print()
print("총 찾은 사진:", f"기본 모델 {found['base']}/{len(photo_names)}장, 내 모델 {found['mine']}/{len(photo_names)}장")
print("결과 폴더:", run_dir)
