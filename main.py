import cv2
import numpy as np
import classifier
import pygame

pygame.init()
screen = pygame.display.set_mode((900,600))
classifier = classifier.Classifier()

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

def predictShapeFromCamera():
    camera = cv2.VideoCapture(0)

    while True:
        ret, frame = camera.read()
        preprocessed_frame = classifier.showCamera(frame)
        label, confidence = classifier.predictShape(preprocessed_frame)

        # Listen to the keyboard for presses.
        keyboard_input = cv2.waitKey(1)

        # 27 is the ASCII for the esc key on your keyboard.
        if keyboard_input == 27:
            break

        # Print prediction and confidence score for debugging(?)
        print("Class:", label, end=" ")
        print("Confidence Score:", str(np.round(confidence * 100))[:-2], "%")

    camera.release()
    cv2.destroyAllWindows()



        