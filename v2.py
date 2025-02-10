import subprocess
import threading
import time
import random
import vlc
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# Function to execute a Python script
def execute_script(script_name):
    """Execute a Python script."""
    print(f"Executing {script_name}...")
    subprocess.run(["python3", script_name])
    print(f"Finished executing {script_name}.")

# State-action mapping
STATE_ACTIONS = {
    "[DAKAEI][STATE] disconnected": ["left.py", "right.py"],
    "[DAKAEI][STATE] speaking": ["left.py", "right.py"],  # Random choice for speaking
    "[DAKAEI][STATE] listening": ["listening.py"],
    "[DAKAEI][STATE] thinking": ["listening.py"]  # Replace thinking.py with led.py
}

def play_intro_video():
    """Play the intro video using VLC."""
    video_url = "intro.mp4"  # Ensure the path to intro.mp4 is correct
    print("Playing intro video...")
    player = vlc.MediaPlayer(video_url)
    player.set_fullscreen(True)
    player.play()

    # Wait until the video finishes playing
    while True:
        state = player.get_state()
        if state in (vlc.State.Ended, vlc.State.Stopped):
            break
        time.sleep(1)

    player.stop()
    player.release()
    print("Intro video finished.")

def monitor_console_logs():
    """Monitor Chromium console logs and execute actions based on states."""
    url = "http://robotum.vercel.app"
    print("Launching Chromium with console log monitoring...")

    # Enable browser console log capture
    capabilities = DesiredCapabilities.CHROME
    capabilities['goog:loggingPrefs'] = {'browser': 'ALL'}

    # Set up Chromium WebDriver options
    options = webdriver.ChromeOptions()
    options.add_argument("--kiosk")  # Fullscreen kiosk mode
    options.add_argument("--disable-infobars")
    options.add_argument("--noerrdialogs")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--use-fake-ui-for-media-stream")  # Allow mic access
    options.add_argument("--enable-features=WebRTCPipeWireCapturer")  # Ensure compatibility with real mic
    options.add_argument("--disable-blink-features=AutomationControlled")  # Remove automation message
    options.add_argument("--enable-blink-features=WebRTCPeerConnection")

    # Path to the Chromium WebDriver
    driver_path = "/usr/bin/chromedriver"

    # Launch the browser
    driver = webdriver.Chrome(executable_path=driver_path, options=options, desired_capabilities=capabilities)

    # Remove the `navigator.webdriver` property (removes automation traces)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    # Open the target URL and set media permissions
    driver.get(url)
    driver.execute_script("""
        navigator.mediaDevices.getUserMedia({ audio: true, video: false })
        .then(stream => console.log('Microphone is working!'))
        .catch(err => console.error('Microphone error:', err));
    """)

    try:
        # Monitor console logs continuously
        active_threads = {}  # To track running threads for states
        while True:
            logs = driver.get_log("browser")
            for entry in logs:
                message = entry["message"]
                for state, actions in STATE_ACTIONS.items():
                    if state in message:
                        print(f"Detected state: {state}")
                        if state == "[DAKAEI][STATE] speaking":
                            # Randomly choose between left.py and right.py
                            chosen_action = random.choice(actions)
                            print(f"Randomly chosen action for speaking: {chosen_action}")
                            execute_script(chosen_action)
                        elif state not in active_threads or not active_threads[state].is_alive():
                            # Launch a thread for each action
                            def run_actions():
                                for action in actions:
                                    execute_script(action)

                            thread = threading.Thread(target=run_actions, daemon=True)
                            thread.start()
                            active_threads[state] = thread

            time.sleep(1)  # Poll logs every second

    except KeyboardInterrupt:
        print("Stopping Chromium...")
    finally:
        driver.quit()

if __name__ == "__main__":
    # Play the intro video
    play_intro_video()

    # Monitor console logs and handle states
    monitor_console_logs()
