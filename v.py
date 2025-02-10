import subprocess
import threading
import time
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
    "[DAKAEI][STATE] speaking": ["speaking.py"],
    "[DAKAEI][STATE] listening": ["listening.py"]
}

# Function to launch Chromium and monitor console logs
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

    # Path to the Chromium WebDriver
    driver_path = "/usr/bin/chromedriver"

    # Launch the browser
    driver = webdriver.Chrome(executable_path=driver_path, options=options, desired_capabilities=capabilities)
    driver.get(url)  # Open the target URL

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
                        if state not in active_threads or not active_threads[state].is_alive():
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
    # Monitor console logs and handle states
    monitor_console_logs()
