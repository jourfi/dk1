import cv2
from gpiozero import OutputDevice
import time
import numpy as np

# GPIO and Motor Setup
IN1 = 14
IN2 = 15
IN3 = 18
IN4 = 23

# Motor constants
DEG_PER_STEP = 1.8
STEPS_PER_REVOLUTION = int(360 / DEG_PER_STEP)

# Create OutputDevice instances
in1 = OutputDevice(IN1)
in2 = OutputDevice(IN2)
in3 = OutputDevice(IN3)
in4 = OutputDevice(IN4)

# Stepper sequence
seq = [
    [1, 0, 0, 1],
    [1, 0, 0, 0],
    [1, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1]
]

def step(delay, step_sequence):
    in1.value = step_sequence[0]
    in2.value = step_sequence[1]
    in3.value = step_sequence[2]
    in4.value = step_sequence[3]
    time.sleep(delay)

def step_forward(steps):
    for _ in range(steps):
        for s in seq:
            step(0.001, s)

def step_backward(steps):
    for _ in range(steps):
        for s in reversed(seq):
            step(0.001, s)

def main():
    # Initialize camera
    cap = cv2.VideoCapture(0)
    
    # Load face detection classifier
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    # Get camera frame width
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    center_x = frame_width // 2
    
    # Define tracking parameters
    dead_zone = 50  # pixels from center where no movement occurs
    steps_per_adjustment = 2  # number of steps to move for each adjustment
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
                
            # Convert to grayscale for face detection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Detect faces
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)
            
            # Process the largest face if any are detected
            if len(faces) > 0:
                # Find the largest face
                largest_face = max(faces, key=lambda x: x[2] * x[3])
                x, y, w, h = largest_face
                
                # Calculate face center
                face_center_x = x + w//2
                
                # Draw rectangle around face and center line
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                cv2.line(frame, (face_center_x, 0), (face_center_x, frame.shape[0]), (0, 255, 0), 1)
                
                # Calculate offset from center
                offset = face_center_x - center_x
                
                # Move motor if face is outside dead zone
                if abs(offset) > dead_zone:
                    if offset > 0:
                        step_backward(steps_per_adjustment)
                    else:
                        step_forward(steps_per_adjustment)
            
            # Draw center reference line
            cv2.line(frame, (center_x, 0), (center_x, frame.shape[0]), (0, 0, 255), 1)
            
            # Display the frame
            cv2.imshow('Face Tracking', frame)
            
            # Break loop on 'q' press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
    except KeyboardInterrupt:
        print("\nExiting the script.")
        
    finally:
        # Cleanup
        cap.release()
        cv2.destroyAllWindows()
        in1.close()
        in2.close()
        in3.close()
        in4.close()

if __name__ == "__main__":
    main() 