import os
from ultralytics import YOLO

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)

PHOTO = "sample_photos/plate_01.jpg"

model = YOLO("yolo26n.pt")
result = model(PHOTO)[0]
result.show()
print(model.names)