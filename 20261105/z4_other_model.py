from ultralytics import YOLO

# ---- 내가 바꾸는 값 ----
PHOTO = "street.jpg"                    # 같은 폴더에 있는 사진 이름 (따옴표 안에 쓴다) : 다음에는 "desk.jpg" 로도 해 본다
MODEL = "yolo26n.pt"                    # 모델 파일 : "yolo26n.pt" (80가지) 또는 "yolov8n-oiv7.pt" (601가지, 처음 쓸 때 자동으로 내려받는다)
CONF = 0.25                             # 자신감 기준

model = YOLO(MODEL)                     # 고른 모델 파일을 불러와 model 이라는 이름을 붙인다
result = model(PHOTO, conf=CONF)[0]     # 사진을 보여 주고 첫째 답을 꺼낸다

print(MODEL, "는", len(model.names), "가지 이름을 안다")
for box in result.boxes:                # 남은 네모를 하나씩 꺼낸다
    name = result.names[int(box.cls[0])]
    print("   ", name, round(float(box.conf[0]), 2))
result.save("yolo_model.jpg")           # 네모를 그린 사진을 파일로 저장한다
print("yolo_model.jpg 로 저장했다")
