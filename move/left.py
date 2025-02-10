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
def step(delay, step_sequence):
    in1.value = step_sequence[0]  # Step 1
    in2.value = step_sequence[1]  # Step 2
    in3.value = step_sequence[2]  # Step 3
    in4.value = step_sequence[3]  # Step 4
    time.sleep(delay)

# Function to move the stepper motor one step forward
def step_forward(delay, steps):
    for _ in range(steps):
        for s in seq:  # Passing the actual sequence
            step(delay, s)

# Function to move the stepper motor one step backward
def step_backward(delay, steps):
    for _ in range(steps):
        for s in reversed(seq):  # Passing the actual sequence in reverse
            step(delay, s)

try:
    # Set a faster delay (for example, 0.005 seconds per step)
    delay = 0.005  # Faster movement
    start_time = time.time()  # Record start time
    total_steps = 0  # Keep track of steps taken
    
    # First phase: Rotate backward for 5 seconds
    while True:
        if time.time() - start_time >= 5:
            break
            
        step_backward(delay, STEPS_PER_REVOLUTION)
        total_steps += STEPS_PER_REVOLUTION

    print("\nReturning to starting position...")
    
    # Second phase: Return to starting position
    step_forward(delay, total_steps)
    print("Returned to starting position")

except KeyboardInterrupt:
    print("\nExiting the script.")

finally:
    # Cleanup the GPIO pins
    in1.close()
    in2.close()
    in3.close()
    in4.close()
