import vlc
import os
import time
import subprocess
import threading

def play_intro_video():
    """Play the intro video using VLC."""
    video_url = "intro.mp4"
    player = vlc.MediaPlayer(video_url)
    player.set_fullscreen(True)
    player.play()

    while True:
        state = player.get_state()
        if state == vlc.State.Ended:
            break
        time.sleep(1)

    player.stop()
    player.release()

def launch_chromium():
    """Launch Chromium in fullscreen mode."""
    url = "http://robotum.vercel.app"
    print("Launching Chromium...")
    os.system(f"chromium-browser --noerrdialogs --disable-infobars --kiosk {url}")
    print("Chromium launched.")

def run_right():
    """Run right.py one time."""
    print("Running right.py...")
    subprocess.run(["python3", "right.py"])
    print("Finished running right.py.")

if __name__ == "__main__":
    # Play the intro video
    play_intro_video()

    # Run Chromium and right.py simultaneously
    threading.Thread(target=launch_chromium, daemon=True).start()
    run_right()
