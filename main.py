import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk
import classifier
import pygame
import time
import random 
import threading

# Initialize Audio
pygame.mixer.init()
pygame.mixer.music.load("audios/incorrect.wav")

# Initialize Classifier
classifier = classifier.Classifier()
conf_threshold = 0.85

is_running = False 

# Each step: video + target
video_steps = [
    {"video":"videos/intro_green_square.mov", "target":"green square"},
    {"video":"videos/red_square.mov", "target":"red square"},
    {"video":"videos/green_triangle.mov", "target":"green triangle"},
    {"video":"videos/blue_circle.mov", "target":"blue circle"},
    {"video":"videos/yellow_star.mov", "target":"yellow star"},
    {"video":"videos/ending.mov", "target":None}
]

# Data for the quiz, all of it is in lowercase following our label
all_shapes = [
    "blue triangle", "green triangle", "red triangle", "yellow triangle",
    "blue circle", "green circle", "red circle", "yellow circle",
    "blue square", "green square", "red square", "yellow square",
    "blue star", "green star", "red star", "yellow star"
]

def predictShapeFromCamera(target_shape):
    global score, is_running

    camera = cv2.VideoCapture(0) 
    # For audio playback delay
    last_played_time = 0
    delay_playback = 4

    # For detection frame counting (to avoid false positives due to quick movements)
    detection_frames = 0
    
    #Modified #1/8/2026 : This is used to show the window for the quiz
    classifier.center_window("Show Me The Shape!", 600, 600)

    while True:
        # 1. STOP CHECK
        if not is_running:
            break

        ret, frame = camera.read()
        if not ret: break

        preprocessed_frame = classifier.showCamera(frame, text_overlay=target_shape)
        label, confidence = classifier.predictShape(preprocessed_frame)
        current_time = time.time()

        keyboard_input = cv2.waitKey(1)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # 4. SUCCESS LOGIC
        if label == target_shape and confidence >= conf_threshold:
            detection_frames += 1
            print(f"Detecting... {detection_frames}/30")
            
            if detection_frames >= 30:
                print(f"Correct! Found {target_shape}")
                score += 1
                root.after(0, lambda: score_label.config(text=f"Score: {score}"))
                break
        else:
            detection_frames = 0
            
            # 5. INCORRECT AUDIO LOGIC
            if label != target_shape and label != "no item" and label != "hand" and confidence >= conf_threshold:
                if current_time - last_played_time > delay_playback:
                    pygame.mixer.music.play()
                    last_played_time = current_time

    camera.release()
    cv2.destroyAllWindows()

def playStory():
    global score, is_running
    score = 0 
    root.after(0, lambda: score_label.config(text=f"Score: {score}"))

    for i, step in enumerate(video_steps):
        if not is_running: break
        
        root.after(0, lambda val=i: progress.configure(value=val))
        
        video_path = step["video"]
        target_shape = step["target"]

        time.sleep(0.5)
        if not is_running: break

        # Play Video 
        from video_player import VideoPlayer
        player = VideoPlayer()
        
        # We pass a lambda function so the video player knows when to quit, 
        #without stop_check it will genuinely not respond.
        player.PlayVideo(video_path, stop_check=lambda: not is_running)

        if not is_running: break
        
        if target_shape is not None:
            predictShapeFromCamera(target_shape)
    
    if is_running: 
        root.after(0, lambda: label.config(text="Story Finished!"))
        root.after(0, lambda: progress.configure(value=len(video_steps)))

def playQuiz():
    global score
    score = 0
    root.after(0, lambda: score_label.config(text=f"Score: {score}"))
    
    questions = random.sample(all_shapes, 5) 
    root.after(0, lambda: progress.configure(maximum=len(questions)))

    for i, target in enumerate(questions):
        if not is_running: break
        
        root.after(0, lambda t=target, idx=i: label.config(text=f"Quiz {idx+1}/{len(questions)}: Show me {t}"))
        root.after(0, lambda val=i: progress.configure(value=val))
        
        predictShapeFromCamera(target)
        
    if is_running: 
        root.after(0, lambda: label.config(text=f"Quiz Done! Final Score: {score}/{len(questions)}"))
        root.after(0, lambda: progress.configure(value=len(questions)))

def reset_and_run(target_function):
    """Kills existing threads safely, waits, then starts new one"""
    global is_running
    
    # 1. Signal threads to stop
    is_running = False 
    
    # NOTE: We do NOT call cv2.destroyAllWindows() here. 
    # We let the background thread close its own windows to prevent crashes.
    
    # 2. Disable buttons
    start_btn.config(state="disabled")
    quiz_btn.config(state="disabled")

    def run_sequence():
        global is_running
        
        time.sleep(1.0) 
        
        is_running = True
        
        root.after(0, lambda: start_btn.config(state="normal"))
        root.after(0, lambda: quiz_btn.config(state="normal"))
        
        target_function()

    threading.Thread(target=run_sequence, daemon=True).start()

# --- UI SETUP ---
root = tk.Tk()
root.title("Shape Story Adventure")
root.geometry("520x450") 
root.resizable(False, False)

score = 0

label = tk.Label(root, text="Select a Mode", font=("Arial", 14))
label.pack(pady=10)

score_label = tk.Label(root, text="Score: 0", font=("Arial", 12))
score_label.pack()

progress = ttk.Progressbar(root, length=300, maximum=10)
progress.pack(pady=10)

# BUTTONS
btn_frame = tk.Frame(root)
btn_frame.pack(pady=20)

start_btn = tk.Button(btn_frame, text="START STORY", font=("Arial", 12), bg="#dddddd", width=15, 
                      command=lambda: reset_and_run(playStory))
start_btn.grid(row=0, column=0, padx=10)

quiz_btn = tk.Button(btn_frame, text="START QUIZ", font=("Arial", 12), bg="#dddddd", width=15, 
                     command=lambda: reset_and_run(playQuiz))
quiz_btn.grid(row=0, column=1, padx=10)

root.mainloop()