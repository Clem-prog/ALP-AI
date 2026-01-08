from keras.models import load_model
import cv2
import numpy as np
import ctypes 

class Classifier:
    def __init__(self):
        self.model = load_model("model/keras_model.h5", compile=False) 
        self.class_names = open("model/labels.txt").readlines()

    def predictShape(self, frame):
        prediction = self.model.predict(frame)
        index = np.argmax(prediction)

        class_name = self.class_names[index][2:].strip().lower()
        confidence_score = float(prediction[0][index])

        return class_name, confidence_score
    
    def showCamera(self, frame, text_overlay=None):
        # this is to remove black bars since we're using droidcam
        # (droidcam generates black bars to the top and bottom of the frame for some reason 😓) 
        h, w, _ = frame.shape
        top_crop = int(0.13 * h)
        bottom_crop = int(0.13 * h)
        frame = frame[top_crop : h - bottom_crop, :]

        # cropping to center square, and shifted right because my phone camera is funny
        h, w, _ = frame.shape
        side = min(h, w)

        shift_right = int(0.05 * w)

        start_x = (w - side) // 2 + shift_right
        start_y = (h - side) // 2

        # Clamp to frame bounds (important)
        start_x = max(0, min(start_x, w - side)) 

        # Resize the raw frame into (224-height,224-width) pixels
        frame = frame[start_y : start_y + side, start_x : start_x + side]

        display = cv2.resize(frame, (400, 400))

        if text_overlay:
            # Black Box
            cv2.rectangle(display, (0,0), (400, 40), (0,0,0), -1)
            # Text
            cv2.putText(display, f"Find: {text_overlay}", (10, 30), 
                        cv2.FONT_HERSHEY_DUPLEX, 0.7, (255, 255, 255), 1)

        # Resize the raw frame into (224-height,224-width) pixels
        frame = cv2.resize(frame, (224, 224), interpolation=cv2.INTER_AREA)

        # Show the frame in a window
        cv2.imshow("Show Me The Shape!", display)

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        frame = np.asarray(frame, dtype=np.float32).reshape(1, 224, 224, 3)

        frame = (frame / 127.5) - 1

        return frame
    
    def center_window(self, window_name, win_w, win_h):
        # Modified 1/8/2026 : high chance we need to channge to ctypes since tkinter will crashed if we change from story to quiz
        user32 = ctypes.windll.user32 
        screen_w = user32.GetSystemMetrics(0)
        screen_h = user32.GetSystemMetrics(1)
        
        x = (screen_w - win_w) // 2
        y = (screen_h - win_h) // 2
        
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(window_name, win_w, win_h)
        cv2.moveWindow(window_name, x, y)