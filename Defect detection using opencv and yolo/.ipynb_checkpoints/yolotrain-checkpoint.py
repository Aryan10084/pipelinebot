from ultralytics import YOLO

# Load a pre-trained YOLOv8 model or create a new one
model = YOLO('yolov8n.pt')  # YOLOv8 nano model (lightweight)

# Train the model with your dataset
model.train(data='C:\Users\DELL\Downloads\Storm drain model.v1-stormdrainmodel_2021-10-22.yolov8\data.yaml', epochs=50)
