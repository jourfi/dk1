import vlc
import os
import time

def play_intro_video():
    # URL of the intro video
    video_url = "intro.mp4"
    
    # Initialize VLC player
    player = vlc.MediaPlayer(video_url)
    player.set_fullscreen(True)
    
    # Start playing the video
    player.play()
    
    # Wait for the video to finish playing
    while True:
        state = player.get_state()
        if state == vlc.State.Ended:
            break  # Exit the loop when the video ends
        time.sleep(1)
    
    # Stop and release the player
    player.stop()
    player.release()

def launch_chromium():
    url = "http://robotum.vercel.app"
    # Launch Chromium in kiosk mode
    os.system(f"chromium-browser --noerrdialogs --disable-infobars --kiosk {url}")

if __name__ == "__main__":
    play_intro_video()
    launch_chromium()
