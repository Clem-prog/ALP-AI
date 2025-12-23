import cv2
import numpy as np
import pygame
import classifier
import time

pygame.mixer.init()
pygame.mixer.music.load("audios/incorrect.wav")

classifier = classifier.Classifier()
camera = cv2.VideoCapture(0)

target_shape = "red square"  # Example target shape
conf_threshold = 0.85

last_played_time = 0
delay_playback = 4

detection_frames = 0

while True:
    ret, frame = camera.read()
    preprocessed_frame = classifier.showCamera(frame)
    label, confidence = classifier.predictShape(preprocessed_frame)

    current_time = time.time()

    # Listen to the keyboard for presses.
    keyboard_input = cv2.waitKey(1)

    # 27 is the ASCII for the esc key on your keyboard (also to simulate success).
    if keyboard_input == 27 or (label == target_shape and confidence >= conf_threshold and detection_frames >= 30):
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