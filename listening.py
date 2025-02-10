from gpiozero import PWMLED
from time import sleep
import math

# Set up LED on GPIO pin 17 as PWM
led = PWMLED(17)

# One complete fade cycle
# Fade in
for i in range(100):
    brightness = math.sin(i * math.pi / 200)
    led.value = brightness
    sleep(0.1)  # Slower fade - adjust this value as needed
    
# Fade out
for i in range(100, 0, -1):
    brightness = math.sin(i * math.pi / 200)
    led.value = brightness
    sleep(0.1)  # Slower fade - adjust this value as needed

# Clean up
led.close()
