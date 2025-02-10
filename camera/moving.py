import cv2
import time
import subprocess
from collections import Counter

# Load the pre-trained Haar cascade for face detection
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Initialize the webcam (default camera index is 0)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

print("Tracking face position for 5 seconds...")

# Start the timer and initialize variables
start_time = time.time()
positions = []

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    if not ret:
        print("Error: Failed to capture frame.")
        break

    # Resize the frame to fit smaller screens
    frame = cv2.resize(frame, (640, 480))

    # Convert the frame to grayscale (Haar cascades work with grayscale images)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Only process the first detected face
    if len(faces) > 0:
        (x, y, w, h) = faces[0]
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Determine the position of the face relative to the center
        frame_center_x = frame.shape[1] // 2
        face_center_x = x + w // 2

        if face_center_x < frame_center_x - 50:
            positions.append("left")
        elif face_center_x > frame_center_x + 50:
            positions.append("right")
        else:
            positions.append("center")

    # Display the resulting frame
    cv2.imshow('Webcam Face Tracking', frame)

    # Break the loop if 'q' is pressed or after 5 seconds
    if cv2.waitKey(1) & 0xFF == ord('q') or (time.time() - start_time > 5):
        break

# Release the webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()

# Determine the most frequent position
if positions:
    most_common = Counter(positions).most_common(1)[0][0]
    print(f"Most frequent position: {most_common}")

    # Execute corresponding script
    if most_common == "left":
        subprocess.run(["python3", "right.py"])
    elif most_common == "right":
        subprocess.run(["python3", "left.py"])
else:
    print("No face detected during the 5 seconds.")
