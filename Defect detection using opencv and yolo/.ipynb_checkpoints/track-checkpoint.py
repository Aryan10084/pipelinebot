import cv2
import numpy as np

# Choose simulation type: 'synthetic_image' or 'dynamic_frames'
SIMULATION_TYPE = "dynamic_frames"  # Change to "synthetic_image" if needed

def generate_dynamic_frame():
    """
    Generate a dynamic frame with random defects (red circles).
    """
    frame = np.ones((480, 640, 3), dtype=np.uint8) * 255  # White background
    for _ in range(5):  # Add 5 random defects
        center = (np.random.randint(50, 590), np.random.randint(50, 430))
        radius = np.random.randint(5, 20)  # Generate random radius
        cv2.circle(frame, center, radius, (0, 0, 255), -1)  # Red defect
    return frame

def detect_defects(frame):
    """
    Detect defects in the frame using color thresholding.
    """
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_red = np.array([0, 120, 70])
    upper_red = np.array([10, 255, 255])
    mask1 = cv2.inRange(hsv, lower_red, upper_red)

    lower_red2 = np.array([170, 120, 70])
    upper_red2 = np.array([180, 255, 255])
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

    mask = mask1 | mask2

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    defects = []

    for contour in contours:
        if cv2.contourArea(contour) > 20:
            x, y, w, h = cv2.boundingRect(contour)
            defects.append((x, y, w, h))
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Draw bounding box

    return frame, defects

def simulate_camera_on_synthetic_image():
    """
    Simulate a moving camera inspecting a synthetic pipeline image.
    """
    # Create a synthetic pipeline image with random defects
    pipeline_image = np.ones((1000, 640, 3), dtype=np.uint8) * 255  # Large white image
    for _ in range(50):  # Add 50 random defects
        center = (np.random.randint(50, 590), np.random.randint(50, 950))
        radius = np.random.randint(5, 20)
        cv2.circle(pipeline_image, center, (0, 0, 255), -1)  # Red defect

    viewport_height = 480
    y = 0

    while y + viewport_height <= pipeline_image.shape[0]:
        viewport = pipeline_image[y:y + viewport_height, :]  # Camera view
        processed_frame, defects = detect_defects(viewport)
        cv2.imshow("Camera View", processed_frame)

        print(f"Camera Position: y={y}, Defects Detected: {len(defects)}")
        y += 20  # Move camera down
        if cv2.waitKey(100) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

def simulate_dynamic_frames():
    """
    Simulate a camera inspecting dynamically generated frames.
    """
    for frame_no in range(50):  # Generate 50 dynamic frames
        frame = generate_dynamic_frame()
        processed_frame, defects = detect_defects(frame)
        cv2.imshow("Camera View", processed_frame)

        print(f"Frame {frame_no + 1}: Defects Detected: {len(defects)}")
        if cv2.waitKey(100) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

# Main execution
if __name__ == "__main__":
    if SIMULATION_TYPE == "synthetic_image":
        simulate_camera_on_synthetic_image()
    elif SIMULATION_TYPE == "dynamic_frames":
        simulate_dynamic_frames()
