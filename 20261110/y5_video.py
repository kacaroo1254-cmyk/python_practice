import os                               # 폴더·파일 이름을 다루는 도구 상자(os)를 가져온다
from ultralytics import YOLO            # ultralytics 도구 상자에서 YOLO 하나만 꺼낸다

HERE = os.path.dirname(os.path.abspath(__file__))   # 이 파일이 들어 있는 폴더의 전체 주소 (예: my_drone8/d29_photo)
os.chdir(HERE)                          # 파이썬의 작업 위치를 이 폴더로 옮긴다 (결과·모델이 이 폴더에 생기게 한다)

# ---- 내가 바꾸는 값 ----
VIDEO = "street.mp4"                    # 같은 폴더에 있는 영상 이름 (따옴표 안에 쓴다)
CONF = 0.25                             # 자신감 기준 : 자신감이 이 숫자보다 낮은 네모는 버린다 (0 ~ 1 사이)
WANT = "person"                         # 세고 싶은 이름 (따옴표 안에 쓴다)

model = YOLO("yolo26n.pt")              # 가장 작은 YOLO 파일을 불러와 model 이라는 이름을 붙인다
results = model(VIDEO, conf=CONF, stream=True, save=True, verbose=False, project=HERE, name="y5_결과", exist_ok=True)   # 영상을 사진(프레임)이 줄줄이 이어진 것으로 보고 한 장씩 답을 받는다 (project=HERE : 결과를 이 폴더 안에 / name : 결과 폴더 이름 / exist_ok=True : 다시 실행하면 같은 폴더에 덮어쓴다)

frame = 0                               # 지금까지 본 사진(프레임)의 수
total = 0                               # 지금까지 센 WANT 의 합
most = 0                                # 한 장에서 가장 많이 센 수
for result in results:                  # 영상 속 사진을 한 장씩 꺼낸다
    count = 0                           # 이 사진에서 센 WANT 의 수 (사진마다 0 에서 다시 시작)
    for box in result.boxes:            # 이 사진의 네모를 하나씩 꺼낸다
        name = result.names[int(box.cls[0])]    # 이름 번호를 이름 글자로 바꾼다
        if name == WANT:                # 세고 싶은 이름이면
            count = count + 1           # 하나 늘린다
    total = total + count               # 합에 더한다
    if count > most:                    # 지금까지 가장 많으면
        most = count                    # 가장 많이 센 수를 바꾼다
    frame = frame + 1                   # 다음 사진으로 간다

print("영상 속 사진(프레임)의 수 :", frame)
print(WANT, "한 장에서 가장 많았던 수 :", most, "개")
print("사진 한 장 평균 :", round(total / frame, 1), "개")
