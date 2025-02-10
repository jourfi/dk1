from gpiozero import OutputDevice
import time

# Define GPIO pins for ULN2003 driver
IN1 = 14
IN2 = 15
IN3 = 18
IN4 = 23

# Define constants
DEG_PER_STEP = 1.8
STEPS_PER_REVOLUTION = int(360 / DEG_PER_STEP)

# Create OutputDevice instances for each pin
in1 = OutputDevice(IN1)
in2 = OutputDevice(IN2)
in3 = OutputDevice(IN3)
in4 = OutputDevice(IN4)

# Define sequence for 28BYJ-48 stepper motor
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

# Function to rotate the stepper motor one step
def step(delay, step_sequence, step_number):
    in1.value = step_sequence[0]  # Step 1
    in2.value = step_sequence[1]  # Step 2
    in3.value = step_sequence[2]  # Step 3
    in4.value = step_sequence[3]  # Step 4
    print(f"Step {step_number}: {step_sequence}")  # Debugging line to print current step number and sequence
    time.sleep(delay)

# Function to move the stepper motor one step forward (clockwise)
def step_forward(delay, steps):
    step_number = 1
    for _ in range(steps):
        for s in seq:  # Passing the actual sequence
            step(delay, s, step_number)
            step_number += 1

# Function to move the stepper motor one step backward (counterclockwise)
def step_backward(delay, steps):
    step_number = 1
    for _ in range(steps):
        for s in reversed(seq):  # Passing the actual sequence in reverse
            step(delay, s, step_number)
            step_number += 1

try:
    # Set an extremely fast delay (0.001 seconds per step)
    delay = 0.001  # Very fast movement (adjust if motor skips steps)
    start_time = time.time()  # Record start time
    total_steps = 0  # Keep track of steps taken
    
    # First phase: Rotate to the right (clockwise) for 5 seconds
    while True:
        if time.time() - start_time >= 5:
            break
            
        step_forward(delay, STEPS_PER_REVOLUTION)  # Rotate to the right
        total_steps += STEPS_PER_REVOLUTION

    print("\nReturning to starting position...")

    # Second phase: Return to the starting position (move left/counterclockwise)
    if total_steps == 0:
        print("Steps reset to zero. Returning to origin...")
        step_backward(delay, STEPS_PER_REVOLUTION)  # Rotate back to the left
        print("Returned to starting position")
    else:
        step_backward(delay, total_steps)  # Rotate back to the left
        print("Returned to starting position")

except KeyboardInterrupt:
    print("\nExiting the script.")

finally:
    # Cleanup the GPIO pins
    in1.close()
    in2.close()
    in3.close()
    in4.close()
