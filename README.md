# Baby Care Monitor

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![OpenCV](https://img.shields.io/badge/OpenCV-27338e?style=for-the-badge&logo=OpenCV&logoColor=white) ![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green) ![Line](https://img.shields.io/badge/Line-00C300?style=for-the-badge&logo=line&logoColor=white)

- Topic 1: 透過 AI 技術辨識嬰兒姿態
- Topic 2: 結合 Line 應用發出通知

## Contribute

[![GitHub](https://badgen.net/badge/icon/YunTW?icon=github&label)](https://github.com/YunTW) [![GitHub](https://badgen.net/badge/icon/BradyFan?icon=github&label)](https://github.com/BradyFan) [![GitHub](https://badgen.net/badge/icon/BrianLiu?icon=github&label)](https://github.com/brianvan555) [![GitHub](https://badgen.net/badge/icon/Uricorn?icon=github&label)](https://github.com/Uricorn99) [![GitHub](https://badgen.net/badge/icon/IvanHsiao?icon=github&label)](https://github.com/IvanHsiao29) [![GitHub](https://badgen.net/badge/icon/Jelly?icon=github&label)](https://github.com/Jelley123)

## Requirement

- Python 3.10.13
- CUDA Toolkit 11.0.3
- cuDNN v8.0.5

## Install

- Numpy
  
  ```bash
  pip install numpy
  ```

- OpenCV

  ```bash
  pip install opencv-python
  pip install opencv-contrib-python
  ```

- Django

  ```bash
  pip install Django
  ```

- Mediapipe
  
  ```bash
  pip install mediapipe
  ```

- Torch
  
  ```bash
  pip install torch==2.0.1
  ```

- Torchvision

  ```bash
  pip install torchvision==0.15.2
  ```

- Do it in once

  ```bash
  pip install numpy opencv-python opencv-contrib-python Django mediapipe torch==2.0.1 torchvision==0.15.2
  ```

## YOLO (You Only Look Once)

![YOLO](https://miro.medium.com/v2/resize:fit:2792/format:webp/1*Co8xD0IWPaBiWr-Xfu38dw.jpeg)

<br>

:link:[YOLOv4 (608x608 batch=1 – 62 FPS on V100) object detection (model is trained on MSCOCO dataset)](https://alexeyab84.medium.com/yolov4-the-most-accurate-real-time-neural-network-on-ms-coco-dataset-73adfd3602fe)

## MediaPipe

![MediaPipe-Face](https://developers.google.com/static/mediapipe/images/solutions/examples/face_landmarker_720.png)

<br>

:link:[Face Landmark Detection](https://mediapipe-studio.webapps.google.com/demo/face_landmarker)

![MediaPipe-Pose](https://developers.google.com/static/mediapipe/images/solutions/examples/pose_detector_720.png)

<br>

:link:[Pose Landmark Detection](https://mediapipe-studio.webapps.google.com/demo/pose_landmarker)

## Usage

1. 準備YOLO需要的檔案，建立一個目錄 ./weights 並下載解壓縮放在目錄內

   - [weights](https://drive.google.com/drive/folders/1RxjkyTuoJ6ESHTZqOCaTNsD5cBGrgN4s?usp=drive_link): 訓練後的模型權重檔案 (ex: .weights)

2. Run Django server

   ```bash
   python manage.py runserver
   ```

3. Web UI![Web UI](./img/WebUI.png)
