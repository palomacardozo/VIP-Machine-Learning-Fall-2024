import cv2
import numpy as np
import subprocess
import datetime
import yt_dlp

# Function to get the direct stream URL using yt-dlp
def get_stream_url(youtube_url):
    ydl_opts = {
        'format': 'best',  # Select the best available format
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(youtube_url, download=False)
        video_url = info_dict.get("url", None)
    return video_url

stream_url = get_stream_url("https://www.youtube.com/watch?v=OlwC1weFdAg")
cap = cv2.VideoCapture(stream_url)
motion_threshold = 100

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
    # Calculate the difference between the current frame and the previous frame
    frame_delta = cv2.absdiff(previous_frame, gray)

    # Apply a threshold to the difference to create a binary image
    thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]

    # Dilate the thresholded image to fill in small holes
    kernel = np.ones((5, 5), np.uint8)  # Create a kernel for dilation
    thresh = cv2.dilate(thresh, kernel, iterations=2)

    #Find contours of the thresholded image
    contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Check if significant motion is detected based on contour areas
    motion_detected = False
    for contour in contours:
        if cv2.contourArea(contour) > motion_threshold:
            motion_detected = True
            break

    # If motion is detected, save the clip
    if motion_detected:
        print("Motion detected! Saving clip...")
        saveclip()

    previous_frame = gray

cap.release()
cv2.destroyAllWindows()
