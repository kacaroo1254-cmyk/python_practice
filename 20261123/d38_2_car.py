import os
import cv2
from ultralytics import YOLO

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)

PHOTO = "sample_photos/plate_01.jpg"

car_model = YOLO("yolo26n.pt")
plate_model = YOLO("plate_best.pt")

car_result = car_model(PHOTO)[0]
plate_result = plate_model(PHOTO)[0]

picture = car_result.plot()
picture = plate_result.plot(img=picture)

cv2.imwrite("result.jpg", picture)
cv2.imshow("result", picture)
cv2.waitKey(0)

