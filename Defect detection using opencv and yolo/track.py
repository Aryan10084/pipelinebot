import cv2
from ultralytics import YOLO

# Load your trained YOLOv8 model
model = YOLO(r'runs\detect\train3\weights\best.pt')  # Provide the correct path to the trained weights

# Open the video file or capture from a webcam
cap = cv2.VideoCapture(r'C:\Users\DELL\Downloads\videoplayback.mp4')  # Replace with the path to your pre-recorded video

# Check if the video is opened correctly
if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

# Initialize the video writer to save the output video
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Using mp4 codec
out = cv2.VideoWriter('output_video.mp4', fourcc, 20.0, (640, 480))  # Adjust frame size if needed

while cap.isOpened():
    ret, frame = cap.read()  # Read a frame from the video
    if not ret:
        break  # If no frame is read, exit the loop

    # Perform object detection on the frame
    results = model(frame)  # Run YOLO model inference

    # Annotate the frame with the detected objects
    annotated_frame = results[0].plot()  # Get annotated frame with bounding boxes

    # Write the annotated frame to the output video file
    out.write(annotated_frame)

    # Optionally, save the annotated frame as an image (if needed)
    # cv2.imwrite('annotated_frame.jpg', annotated_frame)

    # No display of frames via imshow
    # If you want to stop the video manually, press 'q' (optional)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and writer objects
cap.release()
out.release()

# Close any OpenCV windows (if opened)
cv2.destroyAllWindows()

print("Processing complete, output saved to 'output_video.mp4'.")
