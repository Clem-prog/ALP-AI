from keras.models import load_model  # TensorFlow is required for Keras to work
import cv2  # Install opencv-python
import numpy as np

# .venv\Scripts\activate put this in the terminal to activate your virtual environment

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Load the model
model = load_model("model/keras_Model.h5", compile=False)

# Load the labels
class_names = open("model/labels.txt", "r").readlines()

# CAMERA can be 0 or 1 based on default camera of your computer
camera = cv2.VideoCapture(0)

while True:
    # Grab the webcamera's image.
    ret, image = camera.read()

    # this is to remove black bars since we're using droidcam
    # (droidcam adds black bars to the top and bottom of the frame)
    h, w, _ = image.shape
    top_crop = int(0.13 * h)
    bottom_crop = int(0.13 * h)
    image = image[top_crop : h - bottom_crop, :]

    # cropping to center square, shifted right
    h, w, _ = image.shape
    side = min(h, w)

    shift_right = int(0.05 * w)

    start_x = (w - side) // 2 + shift_right
    start_y = (h - side) // 2

    # Clamp to image bounds (important)
    start_x = max(0, min(start_x, w - side))

    image = image[start_y : start_y + side, start_x : start_x + side]

    # Resize the raw image into (224-height,224-width) pixels
    image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)

    image_display = image.copy()

    # Convert BGR → RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Show the image in a window
    cv2.imshow("Webcam Image", image_display)

    # Make the image a numpy array and reshape it to the models input shape.
    image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)

    # Normalize the image array
    image = (image / 127.5) - 1

    # Predicts the model
    prediction = model.predict(image)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]

    # Print prediction and confidence score
    print("Class:", class_name[2:], end="")
    print("Confidence Score:", str(np.round(confidence_score * 100))[:-2], "%")

    # Listen to the keyboard for presses.
    keyboard_input = cv2.waitKey(1)

    # 27 is the ASCII for the esc key on your keyboard.
    if keyboard_input == 27:
        break

camera.release()
cv2.destroyAllWindows()
