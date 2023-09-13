import os
from time import time
import cv2
from mylib.deploy_model import Yolo

# Parameters
cfg_file = "cfg/yolo-obj.cfg"  # 模型配置
data_file = "data/obj.data"  # 資料集路徑
weight_file = "weights/yolo-obj_best.weights"  # 權重

# Yolo 載入模型
yolo = Yolo(config_file=cfg_file, data_file=data_file, weights=weight_file)

cap = cv2.VideoCapture(0)

while cap.isOpened():
    # record start time
    start_time = time()

    ret, frame = cap.read()  # 取得 WebCam 即時畫面

    if not ret:
        break

    # Yolo Object Detection
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image_detection, detections = yolo.Object_Detect(frame_rgb)

    # ----FPS calculation
    fps = int(1 / (time() - start_time))

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

    cv2.imshow("result", image_detection)

    k = cv2.waitKey(1)

    if k == ord("q"):  # 關閉
        break

cv2.destroyAllWindows()  # 關閉所有cv2建立的視窗
cap.release()
