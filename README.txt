=================================================================================================
This program works with Python 3.10 and tensorflow 2.12.0

For the classifier to work more confidently, surroundings should be clean
and there has to be good lighting.

Model is trained by putting 1 shape in 2 surfaces: purple colored binder, and white wood surface,
when using this program, and the shape isn't recognized when putting it in a normal surface, try 
using a surface that is purple.

Camera has to be using droidcam (software to make phone as webcam), if you don't have droidcam
and it doesn't show anything, you may need to change:

cv2.VideoCapture(0) => cv2.VideoCapture(1) from the predictShapeFromCamera function in main.py
(that will use your webcam instead),

For the story: press Q to skip the story/camera segment.

Some libraries to install if unavailable:
pip install ffpyplayer
pip install opencv-python
pip install tensorflow==2.12.0
=================================================================================================
