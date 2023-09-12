import os
from time import time
import cv2
from mylib.deploy_model import Yolo

# 測試資料集路徑
test_path = "C:/Users/user/Downloads/Baby-Detection.v1i.darknet/test/"

test_images = [f for f in os.listdir(test_path) if f.endswith(".jpg")]

# 隨機圖像路徑
import random

img_path = test_path + random.choice(test_images)

# Parameters
cfg_file = "cfg/yolo-obj.cfg"  # 模型配置
data_file = "data/obj.data"  # 資料集路徑
weight_file = "weights/yolo-obj_best.weights"  # 權重

# Yolo 載入模型
yolo = Yolo(config_file=cfg_file, data_file=data_file, weights=weight_file)

# Yolo Object Detection
frame = cv2.imread(img_path)
frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
image_detection = yolo.Object_Detect(frame_rgb)

cv2.imshow("result", image_detection)
cv2.waitKey(0)
