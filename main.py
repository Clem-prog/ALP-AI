import cv2
import numpy as np
import classifier
import pygame
import time

pygame.mixer.init()
pygame.mixer.music.load("audios/incorrect.wav")

classifier = classifier.Classifier()
current_time = time.time()

conf_threshold = 0.85

# Each step: video + target
video_steps = [
    {"video":"videos/intro_green_square.mov", "target":"green square"},
    {"video":"videos/red_square.mov", "target":"red square"},
    {"video":"videos/green_triangle.mov", "target":"green triangle"},
    {"video":"videos/blue_circle.mov", "target":"blue circle"},
    {"video":"videos/yellow_star.mov", "target":"yellow star"},
    {"video":"videos/ending.mov", "target":None}
]

def predictShapeFromCamera(target_shape): #TODO: make this function work with pygame window + have if statement to exit when answer is correct
    
    camera = cv2.VideoCapture(0)

    # For audio playback delay
    last_played_time = 0
    delay_playback = 4

    # For detection frame counting (to avoid false positives due to quick movements)
    detection_frames = 0
    
    while True:
        ret, frame = camera.read()
        preprocessed_frame = classifier.showCamera(frame)
        label, confidence = classifier.predictShape(preprocessed_frame)

        current_time = time.time()

        # Listen to the keyboard for presses.
        keyboard_input = cv2.waitKey(1)

        # this stops the camera after correct shape is detected
        if label == target_shape and confidence >= conf_threshold and detection_frames >= 30:
            break

        # Print prediction and confidence score for debugging(?)
        print("Class:", label, end=" ")
        print("Confidence Score:", str(np.round(confidence * 100))[:-2], "%")

        if label != target_shape and label != "no item" and confidence >= conf_threshold and detection_frames >= 30:
            if current_time - last_played_time > delay_playback:
                pygame.mixer.music.play()
                last_played_time = current_time
            continue

        if confidence >= conf_threshold and label != "no item" and label != "hand":
            detection_frames += 1
        else:
            detection_frames = 0

    camera.release()
    cv2.destroyAllWindows()
    detection_frames = 0
    target_shape = None

def playStory():
    for step in video_steps:
        video_path = step["video"]
        target_shape = step["target"]

        time.sleep(0.5)

        # Play the video
        from video_player import VideoPlayer
        player = VideoPlayer()
        player.PlayVideo(video_path)

        # If there's a target shape, start the camera prediction
        if target_shape is not None:
            classifier.center_window("Show Me The Shape!", 600, 600)
            predictShapeFromCamera(target_shape)

playStory()



        