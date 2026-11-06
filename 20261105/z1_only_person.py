from ultralytics import YOLO

# ---- 내가 바꾸는 값 ----
PHOTO = "street.jpg"                    # 같은 폴더에 있는 사진 이름 (따옴표 안에 쓴다)
CONF = 0.25                             # 자신감 기준 (y2, y3 와 같은 값)
ONLY = [0]                              # 그릴 이름의 번호 : 0 = person (사람), 24 = backpack, 26 = handbag

model = YOLO("yolo26n.pt")              # 가장 작은 YOLO 파일을 불러와 model 이라는 이름을 붙인다
results = model(PHOTO, conf=CONF, classes=ONLY)     # 사진을 보여 준다 : classes 에 적은 번호의 이름만 남긴다
result = results[0]                     # 답 묶음의 0번째 = 사진 한 장에 대한 답

print("번호", ONLY, "만 그렸다 → 남은 네모 :", len(result.boxes), "개")     # len : 남은 네모의 수
result.save("yolo_only.jpg")            # 남은 네모만 그린 사진을 파일로 저장한다
print("yolo_only.jpg 로 저장했다")
