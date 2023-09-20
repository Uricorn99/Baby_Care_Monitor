from django.shortcuts import render
import cv2
from django.http import StreamingHttpResponse
import numpy as np
import time
import logging as log
import datetime as dt
from mylib import computer_vision as cv
from mylib.deploy_model import Yolo
from api.views import *

# cascPath = "C:/Users/jd200/Desktop/facedetection/haarcascade_frontalface_default.xml"
# cascPath = "C:/Users/user/Desktop/facedetection/haarcascade_frontalface_default.xml"
# faceCascade = cv2.CascadeClassifier(cascPath)

# logger
log.basicConfig(filename="webcam.log", level=log.INFO)


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
       
        # 將原始影像轉換為 JPEG 格式
        _, original_buffer = cv2.imencode(".jpg", frame)
        original_frame = original_buffer.tobytes()

        # TODO: web影像大小需要調整
        # 將經過 YOLO 處理的影像轉換為 JPEG 格式
        _, detection_buffer = cv2.imencode(".jpg", image_detection)
        detection_frame = detection_buffer.tobytes()

        yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + original_frame + b"\r\n", detection_frame)



        # # 將原始影像和檢測結果一同串流
        # yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + original_frame + b"\r\n")
        # yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + detection_frame + b"\r\n")

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

# def original_feed(request):
#     return  StreamingHttpResponse(
#         obj_detection_webcam_m(request),
#         content_type='multipart/x-mixed-replace; boundary=frame'
#         )

# def original_stream(request):
#     return render(request, 'mediapipe_video.html', {'video_stream_url': '/original_feed/'})