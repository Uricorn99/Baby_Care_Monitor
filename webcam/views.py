# pylint: disable=bare-except
import logging as log
import datetime as dt
from time import time
import cv2
import threading
import re
from django.shortcuts import render
from django.http import StreamingHttpResponse
from mylib import computer_vision as cv
from mylib.deploy_model import Yolo
from api.views import *
from mylib.line import Notify
from mylib.Mediapipe import MediapipeDetector # 導入 Mediapipe Detector

# logger
log.basicConfig(filename="webcam.log", level=log.INFO)

def obj_detection_webcam(request):
    # Vars
    yolo = Yolo()
    # Mediapipe 偵測器載入
    MediapipeDetector_working = MediapipeDetector()
    # Parameters
    cfg_file = "cfg/yolov4-cfg-train.cfg"  # 模型配置
    data_file = "data/pose.data"  # 資料集路徑
    weight_file = "weights/yolov4-cfg-train_best.weights"  # 權重

    # 建立新的執行緒讓 Yolo 載入模型
    yolo_loadNet_thread = threading.Thread(
        target=yolo.Load_Net, args=(cfg_file, data_file, weight_file)
    )
    # 強制跟主執行緒一起結束
    yolo_loadNet_thread.setDaemon(True)
    # 執行緒開始運行
    yolo_loadNet_thread.start()
    
    # 建構Line notify副執行緒
    task = Notify()
    # global param for line notify
    task.old_result = None
    task.first_alarm = None
    task.data = None
    imageFile = None
    old_send_time = None
    send_thread = threading.Thread(target = task.send_work, args=(task.data, imageFile), daemon=True)
    send_thread.start()
    
    # Open a connection to the default webcam (usually index 0)
    # video_capture = cv2.VideoCapture(0)
    video_capture, video_writer, video_height, video_width = cv.cam_init(0)
    # video_capture, video_writer, video_height, video_width = cv.cam_init(0, True)
    anterior = 0
    old_record = 'false'
    
    # frame_delay = 0.075  # Set the delay between frames (in seconds)

    # 等候執行緒完成
    yolo_loadNet_thread.join()

    while video_capture.isOpened():  # 檢查 cam 是否開啟
        # record start time
        start_time = time()
        # 從網頁端抓取使用者變數
        global_param = get_param()
        print(global_param)
        user_thresh = float(global_param["acc"])
        kt = float(global_param["dangertime"])
        si = float(global_param["warningtime"])*60
        tn = global_param["toggle_notification"]
        record = global_param["recording"]
        # Capture frame-by-frame from the webcam
        ret, frame = video_capture.read()
        
        if not ret:
            
            break
        
        # 影片錄製
        if record == "true" and old_record == "false":
            old_record = record
            now = dt.datetime.now()
            video_name = now.strftime("%Y-%m-%d %H:%M:%S")
            video_name = re.sub(r'[^\w]', '_', video_name)
            # print('start recording')
            _,video_writer, _,_= cv.cam_init(0,is_write=True, save_path=f"{video_name}.avi")
            video_writer.write(frame)
        elif record == "false" and old_record == "true":
            old_record = record
            video_writer.release()
            _,video_writer, _,_= cv.cam_init(is_write=False)
            # print('stop recording')
        elif record == "true" and old_record == "true":
            video_writer.write(frame)
            # print('keep recording')
        else:
            old_record = record
        # print(f'record:{record}, old record:{old_record}')
            
        # 轉換色彩空間 BGR -> RGB
        # frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # TODO: BradyFan 需確認要 Yolo 最終是用原圖疊加骨架或者空白背景骨架
        detection_face, detection_pose = MediapipeDetector_working.run_all(frame) # 透過模型偵測 frame_rgb 的臉跟骨架
        # blank_frame = MediapipeDetector_working.draw_blank(detection_face, detection_pose) # 繪製空白背景骨架圖
        overlay_frame = MediapipeDetector_working.draw_overlay(detection_face, detection_pose) # 原圖疊加骨架圖
        
        # blank_frame_rgb = cv2.cvtColor(blank_frame, cv2.COLOR_BGR2RGB) # 轉換色彩空間 BGR -> RGB
        overlay_frame_rgb = cv2.cvtColor(overlay_frame, cv2.COLOR_BGR2RGB) # 轉換色彩空間 BGR -> RGB
        # frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # 轉換色彩空間 BGR -> RGB

        # Yolo Object Detection
        image_detection, detections = yolo.Object_Detect(overlay_frame_rgb, user_thresh)

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

        # Line Notify
        task.line_notify(detections, kt, si, tn)
        if task.send_time:
            if old_send_time is None or task.send_time != old_send_time:
                old_send_time = task.send_time
                task.q.put((task.data, imageFile), block=True)
                # send_time = task.get_send_time()
        print(task.old_result, task.first_alarm,  task.send_time)

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