import cv2
import numpy as np
#import subprocess
import datetime
#import yt_dlp
import os

# Function to get the direct stream URL using yt-dlp
def get_stream_url(youtube_url):
    import yt_dlp
    ydl_opts = {
        'format': 'best',  # Select the best available format
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(youtube_url, download=False)
        video_url = info_dict.get("url", None)
    return video_url

# YouTube video URL
youtube_url = "https://www.youtube.com/watch?v=OlwC1weFdAg"

# Get the actual video stream URL
stream_url = get_stream_url(youtube_url)

# Open video stream with the direct URL
cap = cv2.VideoCapture(stream_url)
motion_threshold = 500

if not cap.isOpened():
    print("Error: Couldn't open the bee honey project stream.")
    exit()

# Function to save a clip when motion is detected
def saveclip(frames):
    # Get the user's home directory
    home_directory = os.path.expanduser("~")
    # Set the output directory to Desktop
    output_directory = os.path.join(home_directory, "Desktop")
    # Create a timestamp for the output filename
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    outputfilename = os.path.join(output_directory, f"clip_{timestamp}.mp4")

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Use 'XVID' or 'mp4v' for mp4 format
    out = cv2.VideoWriter(outputfilename, fourcc, 20.0, (640, 480))  # Adjust resolution and fps as needed

    # Write frames to the video file
    for frame in frames:
        out.write(frame)

    # Release the VideoWriter object
    out.release()
    print(f"Clip saved: {outputfilename}")

previous_frame = None
recorded_frames = []

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Store the frame for writing later
    recorded_frames.append(frame)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    if previous_frame is None:
        previous_frame = gray
        continue

    frame_delta = cv2.absdiff(previous_frame, gray)
    thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]

    kernel = np.ones((5, 5), np.uint8)
    thresh = cv2.dilate(thresh, kernel, iterations=2)

    contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    motion_detected = False
    for contour in contours:
        if cv2.contourArea(contour) > motion_threshold:
            motion_detected = True
            break

    if motion_detected:
        print("Motion detected! Saving clip...")
        saveclip(recorded_frames)  # Save the recorded frames as a clip
        recorded_frames = []  # Clear the frames after saving

    previous_frame = gray

cap.release()
cv2.destroyAllWindows()