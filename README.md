# Baby Care Monitor

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
  pip install torch
  ```
- Torchvision
  ```bash
  pip install torchvision
  ```
- Do it in once
  ```bash
  pip install numpy opencv-python opencv-contrib-python Django mediapipe torch torchvision
  ```

## Usage
1. 準備YOLO需要的檔案，建立一個目錄 \weights 並下載解壓縮放在目錄內 
   - [weights](https://drive.google.com/drive/folders/1RxjkyTuoJ6ESHTZqOCaTNsD5cBGrgN4s?usp=drive_link): 訓練後的模型權重檔案 (ex: .weights)

2. Run Django server
   ```bash
   python manage.py runserver
   ```
3. Run YOLO demo from file. (Windows App)
   ```bash
   python detection_file_demo.py
   ```
4. Run YOLO demo from cam. (Windows App)
   ```bash
   python detection_cam_demo
   ```