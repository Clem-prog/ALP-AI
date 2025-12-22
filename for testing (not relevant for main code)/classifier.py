from keras.models import load_model
import cv2
import numpy as np

np.set_printoptions(suppress=True)

class ShapeClassifier:

    def __init__(self):
        self.model = load_model("model/keras_Model.h5", compile=False)
        self.class_names = open("model/labels.txt").readlines()

    def predict(self, frame):

        # this is to remove black bars since we're using droidcam
        # (droidcam adds black bars to the top and bottom of the frame)

        h, w, _ = frame.shape
        top_crop = int(0.13 * h)
        bottom_crop = int(0.13 * h)
        frame = frame[top_crop : h - bottom_crop, :]

        # cropping to center square, shifted right
        h, w, _ = frame.shape
        side = min(h, w)
        shift_right = int(0.05 * w)

        start_x = (w - side) // 2 + shift_right
        start_y = (h - side) // 2
        start_x = max(0, min(start_x, w - side))

        frame = frame[start_y : start_y + side, start_x : start_x + side]

        # Resize to model input
        frame = cv2.resize(frame, (224, 224), interpolation=cv2.INTER_AREA)

        # Convert BGR → RGB so that the model can read it
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Normalize
        image = np.asarray(frame, dtype=np.float32)
        image = (image / 127.5) - 1
        image = image.reshape(1, 224, 224, 3)

        prediction = self.model.predict(image)
        index = np.argmax(prediction)

        label = self.class_names[index][2:].strip().lower()
        confidence = float(prediction[0][index])

        return label, confidence
