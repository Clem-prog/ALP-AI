import cv2 
import numpy as np
from ffpyplayer.player import MediaPlayer 
import ctypes 
import tkinter as tk
import time


class VideoPlayer:
    
    # Modified 1/8/2026 : Added stop_check parameter to listen for "Stop" signals from main.py, if this isnt added even if we remove tkinter it will still crash
    def PlayVideo(self, video_path, stop_check=None):
        video = cv2.VideoCapture(video_path)
        player = MediaPlayer(video_path)
        audio_over = False

        vid_w, vid_h = 720, 405 #window playing video should be small + in 16:9

        root = tk.Tk()
        root.withdraw() 
        screen_w = root.winfo_screenwidth()
        screen_h = root.winfo_screenheight()
        

        # Centering the window
        x = (screen_w - vid_w) // 2
        y = (screen_h - vid_h) // 2

        window_name = "The Adventure of Professor Octagon" 
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(window_name, vid_w, vid_h)
        cv2.moveWindow(window_name, x, y)

        time.sleep(0.3) # Give some time for the window to appear so that audio syncs


        while True:
            # FIX: Check if main.py wants us to stop
            if stop_check is not None and stop_check():
                print("Video Force Stopped by User")
                break

            if cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
                print("Video Window Closed")

            audio_frame, val = player.get_frame()
            grabbed, frame = video.read()

            if audio_over != True and (val == 'eof'):
                audio_over = True
                player.toggle_pause()

            if not grabbed:
                print("End of Video")
                break

            frame = cv2.resize(frame, (vid_w, vid_h))
            cv2.imshow(window_name, frame)

            # Allow 'q' key to quit manually
            if cv2.waitKey(12) & 0xFF == ord("q"):
                break
        
        print("Exiting Video Player")
        audio_over = False
        video.release()
        cv2.destroyAllWindows()