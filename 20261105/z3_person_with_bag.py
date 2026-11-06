from ultralytics import YOLO

# ---- 내가 바꾸는 값 ----
PHOTO = "street.jpg"                    # 같은 폴더에 있는 사진 이름 (따옴표 안에 쓴다)
CONF = 0.25                             # 자신감 기준

model = YOLO("yolo26n.pt")              # 가장 작은 YOLO 파일을 불러와 model 이라는 이름을 붙인다
result = model(PHOTO, conf=CONF, classes=[0, 24, 26])[0]     # 사람(0), 배낭(24), 손가방(26) 네모만 남긴다

people = []                             # 사람 네모의 번호표 : 처음에는 비어 있다
bags = []                               # 가방 네모의 번호표
for n in range(len(result.boxes)):      # 남은 네모를 0번, 1번, 2번 ... 순서로 꺼낸다
    if int(result.boxes.cls[n]) == 0:   # 이름 번호가 0 이면 사람
        people.append(n)
    else:                               # 아니면 배낭이나 손가방
        bags.append(n)

keep = []                               # 가방을 가진 사람의 번호표
for p in people:
    px1, py1, px2, py2 = result.boxes.xyxy[p]       # 사람 네모의 왼쪽 위(x1, y1)와 오른쪽 아래(x2, y2) 모서리
    for b in bags:
        bx1, by1, bx2, by2 = result.boxes.xyxy[b]   # 가방 네모의 모서리
        cx = (bx1 + bx2) / 2                        # 가방 네모의 가운데 가로 위치
        cy = (by1 + by2) / 2                        # 가방 네모의 가운데 세로 위치
        if px1 < cx < px2 and py1 < cy < py2:       # 가방의 가운데가 사람 네모 안에 있으면
            keep.append(p)
            break                                   # 이 사람은 찾았으니 다음 사람으로

print("가방을 가진 사람 :", len(keep), "명")
result[keep].save("yolo_person_bag.jpg")            # 그 사람들의 네모만 그려서 저장한다
print("yolo_person_bag.jpg 로 저장했다")
