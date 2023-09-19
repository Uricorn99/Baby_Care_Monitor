from django.shortcuts import render
import cv2
from django.http import StreamingHttpResponse
import numpy as np
import time
import logging as log
import datetime as dt
from mylib import computer_vision as cv
#from mylib.deploy_model import Yolo
from api.views import *

cascPath = "C:/Users/jd200/Desktop/facedetection/haarcascade_frontalface_default.xml"
# cascPath = "C:/Users/user/Desktop/facedetection/haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)
log.basicConfig(filename='webcam.log', level=log.INFO)

def face_detection_m(request):
    video_capture = cv2.VideoCapture("C:/Users/jd200/Desktop/facedetection/2.mp4")
    # video_capture = cv2.VideoCapture("C:/Users/user/Desktop/facedetection/1.mp4")
    anterior = 0

    frame_delay = 0.075  # Set the delay between frames (in seconds)

    while True:
        # param = get_param() 
        # print(param)
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

def original_feed(request):
    return  StreamingHttpResponse(face_detection_m(request), content_type='multipart/x-mixed-replace; boundary=frame')

def original_stream(request):
    return render(request, 'mediapipe_video.html', {'video_stream_url': '/original_feed/'})



# logger
#log.basicConfig(filename="webcam.log", level=log.INFO)


def obj_detection_webcam_m(request):
    # Parameters
    cfg_file = "cfg/yolov4-cfg-train.cfg"  # 模型配置
    data_file = "data/pose.data"  # 資料集路徑
    weight_file = "weights/yolov4-cfg-train_best.weights"  # 權重

    # Yolo 載入模型
    yolo = Yolo(config_file=cfg_file, data_file=data_file, weights=weight_file)

    # Open a connection to the default webcam (usually index 0)
    # video_capture = cv2.VideoCapture(0)
    video_capture, video_writer, video_height, video_width = cv.cam_init(0)

    anterior = 0

    # frame_delay = 0.075  # Set the delay between frames (in seconds)

    while video_capture.isOpened():  # 檢查 cam 是否開啟
        # record start time
        start_time = time()

        # Capture frame-by-frame from the webcam
        ret, frame = video_capture.read()

        if not ret:
            # TODO: 加上異常處理
            break

        # 轉換色彩空間 BGR -> RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Yolo Object Detection
        image_detection, detections = yolo.Object_Detect(frame_rgb)

        # 偵測到物件時紀錄
        if anterior != len(detections):
            anterior = len(detections)
            log.info(
                "Objects: " + str(len(detections)) + " at " + str(dt.datetime.now())
            )

        # ----FPS calculation
        fps = cv.calc_fps(start_time)

        # cv2.putText(影像, 文字, 座標, 字型, 大小, 顏色, 線條寬度, 線條種類)
        cv2.putText(
            image_detection,
            f"FPS {fps}",
            (10, 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.45,
            (0, 255, 0),
            2,
        )

        # TODO: web影像大小需要調整
        # Convert the frame to JPEG format
        _, buffer = cv2.imencode(".jpg", image_detection)
        frame = buffer.tobytes()

        yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")

        # Introduce a delay between frames
        # time.sleep(frame_delay)


def mediapipe_feed(request):
    return StreamingHttpResponse(
        obj_detection_webcam_m(request),
        content_type="multipart/x-mixed-replace; boundary=frame",
    )


def mediapipe_stream(request):
    return render(
        request, "mediapipe_video.html", {"video_stream_url": "/mediapipe_feed/"}
    )
