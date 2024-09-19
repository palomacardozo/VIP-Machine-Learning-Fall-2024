import cv2
import numpy as np
import subprocess
import datetime

stream_url = "https://www.youtube.com/watch?v=OlwC1weFdAg"
cap = cv2.VideoCapture(stream_url)

if not cap.isOpened():
    print("Error: Couldn't open the bee honey project stream.")
    exit()

def saveclip():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    outputfilename = f"clip_{timestamp}.mp4"

    ffmpeg_command = [
        "ffmpeg",
        "-i", stream_url,
        "-t", "10",  # Record for 10 seconds after motion detection
        outputfilename
    ]
    subprocess.run(ffmpeg_command)

previous_frame = None

while True:
    ret, frame = cap.read()
    if not ret:
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    if previous_frame is None:
        previous_frame = gray
        continue
