import ultralytics
from ultralytics import YOLO
ultralytics.checks()

# Load a model
model = YOLO('yolov8m-pose.pt')  # load a pretrained model (recommended for training)

# Train the model
model.train(data='coco8-pose.yaml', epochs=100, imgsz=640)