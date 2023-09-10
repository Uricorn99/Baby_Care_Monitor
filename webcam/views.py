from django.shortcuts import render
import cv2
from django.http import StreamingHttpResponse
import numpy as np
import time
import logging as log
import datetime as dt

cascPath = "C:/Users/User/Downloads/projectname-20230910T064614Z-001/projectname/haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)
log.basicConfig(filename='webcam.log', level=log.INFO)

def face_detection_webcam(request):
    # Open a connection to the default webcam (usually index 0)
    video_capture = cv2.VideoCapture(0)

    anterior = 0

    frame_delay = 0.075  # Set the delay between frames (in seconds)

    while True:
        # Capture frame-by-frame from the webcam
        ret, frame = video_capture.read()

        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )

        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        if anterior != len(faces):
            anterior = len(faces)
            log.info("faces: "+str(len(faces))+" at "+str(dt.datetime.now()))

        # Convert the frame to JPEG format
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        # Introduce a delay between frames
        time.sleep(frame_delay)

def webcam_video_feed(request):
    return StreamingHttpResponse(face_detection_webcam(request), content_type='multipart/x-mixed-replace; boundary=frame')

def webcam_video_stream(request):
    return render(request, 'webcam.html', {'video_stream_url': '/webcam_video_feed/'})
