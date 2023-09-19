# pylint: disable=bare-except
import logging as log
import datetime as dt
from time import time
import cv2
from django.shortcuts import render
from django.http import StreamingHttpResponse
from mylib import computer_vision as cv
from mylib.deploy_model import Yolo
from api.views import *

# logger
log.basicConfig(filename="webcam.log", level=log.INFO)

def obj_detection_webcam(request):
    # Parameters
    cfg_file = "cfg/yolov4-cfg-train_ori.cfg"  # 模型配置
    data_file = "data/pose_ori.data"  # 資料集路徑
    weight_file = "weights/yolov4-cfg-train_ori_best.weights"  # 權重

    # Yolo 載入模型
    yolo = Yolo(config_file=cfg_file, data_file=data_file, weights=weight_file)

    # Open a connection to the default webcam (usually index 0)
    # video_capture = cv2.VideoCapture(0)
    video_capture, video_writer, video_height, video_width = cv.cam_init(0)
    anterior = 0

    # global param for line notify
    old_result = None
    first_alarm = None
    send_time = None
    
    # frame_delay = 0.075  # Set the delay between frames (in seconds)
    while video_capture.isOpened():  # 檢查 cam 是否開啟
        # record start time
        start_time = time()
        # TODO: 從網頁端抓取使用者變數
        global_param = get_param()
        user_thresh = float(global_param["acc"])
        kt = float(global_param["dangertime"])
        si = float(global_param["warningtime"])
        tn = global_param["toggle_notification"]

        # Capture frame-by-frame from the webcam
        ret, frame = video_capture.read()

        if not ret:
            
            break

        # 轉換色彩空間 BGR -> RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Yolo Object Detection
        # TODO: 新增使用者自定義閥值，並取出查看        
        image_detection, detections = yolo.Object_Detect(frame_rgb, user_thresh)
                
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
        imageFile = {'imageFile' : frame}   # 設定圖片資訊

        # TODO: Line Notify
        old_result, first_alarm,  send_time = line_notify(tn,detections,kt,imageFile,si) 
        print(old_result, first_alarm,  send_time)

        yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")

        # Introduce a delay between frames
        # time.sleep(frame_delay)


def webcam_video_feed(request):
    return StreamingHttpResponse(
        obj_detection_webcam(request),
        content_type="multipart/x-mixed-replace; boundary=frame",
    )


def webcam_video_stream(request):
    return render(
        request, "webcam_codepen.html", {"video_stream_url": "/webcam_video_feed/"}
    )
