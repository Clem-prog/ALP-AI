import cv2 # pip install opencv-python
import numpy as np
from ffpyplayer.player import MediaPlayer #pip install ffpyplayer
import tkinter as tk
import time

class VideoPlayer:
    
    def PlayVideo(self, video_path):
        video=cv2.VideoCapture(video_path)
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

        cv2.namedWindow("The Adventure of Professor Octagon", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("The Adventure of Professor Octagon", vid_w, vid_h)
        cv2.moveWindow("The Adventure of Professor Octagon", x, y)

        time.sleep(0.3)  # Give some time for the window to appear so that audio syncs

        while True:
            audio_frame, val = player.get_frame()
            grabbed, frame=video.read()

            print("audio_frame:", audio_frame, "val:", val)
            print("grabbed:", grabbed)

            if audio_over != True and (val == 'eof'):
                audio_over = True
                player.toggle_pause()
                print("Audio Finished")

            if not grabbed:
                print("End of Video")
                break

            frame = cv2.resize(frame, (vid_w, vid_h))
            cv2.imshow("The Adventure of Professor Octagon", frame)

            if cv2.waitKey(12) & 0xFF == ord("q"):
                break
        
        print("Exiting")
        audio_over = False
        video.release()
        cv2.destroyAllWindows()

