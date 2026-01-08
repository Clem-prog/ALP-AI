=================================================================================================
This program works with Python 3.10 and tensorflow 2.12.0

For the classifier to work, surroundings should be clean
and there has to be good lighting.

Camera should be using droidcam, if you don't have droidcam
and it doesn't show anything, you may need to change:

cv2.VideoCapture(0) => cv2.VideoCapture(1) from the predictShapeFromCamera function in main.py
(that will use your webcam instead),

Some libraries to install if unavailable:
pip install ffpyplayer
pip install opencv-python
pip install tensorflow==2.12.0
=================================================================================================

