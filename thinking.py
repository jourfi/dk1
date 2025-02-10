from gpiozero import LED
from time import sleep, time

# Set up LED on GPIO pin 17
led = LED(17)

# Record start time
start_time = time()
duration = 60  # Duration in seconds

# Start with slow blink and get faster
delay = 0.5  # Starting delay (slow blink)
while time() - start_time < duration:
    led.on()
    print("LED ON")
    sleep(delay)
    
    led.off()
    print("LED OFF")
    sleep(delay)
    
    # Make it blink faster by reducing delay
    delay = delay * 0.75  # Reduce delay by 25% each time
    
    # Don't let delay get too small
    if delay < 0.05:
        delay = 0.05

# Ensure LED is off when done
led.off()
