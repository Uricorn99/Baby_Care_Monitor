from django.shortcuts import render
import cv2
import logging as log
import datetime as dt
# from django.http import HttpResponse
from django.http import StreamingHttpResponse
import numpy as np
import time  # Import the time module
from api.views import *

cascPath = "C:/Users/jd200/Desktop/facedetection/haarcascade_frontalface_default.xml"
#cascPath = "C:/Users/user/Desktop/facedetection/haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)
log.basicConfig(filename='webcam.log', level=log.INFO)

def face_detection(request):
    video_capture = cv2.VideoCapture("C:/Users/jd200/Desktop/facedetection/1.mp4")
    #video_capture = cv2.VideoCapture("C:/Users/user/Desktop/facedetection/1.mp4")
    anterior = 0

    frame_delay = 0.075  # Set the delay between frames (in seconds)

    while True:
        param = get_param() 
        print(param)
        # Capture frame-by-frame
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

def video_feed(request):
    return  StreamingHttpResponse(face_detection(request), content_type='multipart/x-mixed-replace; boundary=frame')



def video_stream(request):
    return render(request, 'video_stream.html', {'video_stream_url': '/video_feed/'})