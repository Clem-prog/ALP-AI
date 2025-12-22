import os
os.environ["MOVIEPY_DISABLE_FFPLAY_CHECK"] = "1"

from moviepy import VideoFileClip

clip = VideoFileClip("./videos/green_triangle.mov").resized((1920, 1080))
clip.preview()