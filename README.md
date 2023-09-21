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
1. 準備YOLO需要的檔案，下載解壓縮放在專案內
   - [cfg](https://drive.google.com/file/d/1TVv__CZvOPY8VBLIb7eCy5WCefpty5N6/view?usp=drive_link): 模型參數 (ex: .cfg)
   - [data](https://drive.google.com/file/d/1-FA0MlWu5gCMVYkGCFd-pKGCdrCZB1m8/view?usp=drive_link), [name](https://drive.google.com/file/d/1-AvngQVa06aCxEgs9tP0JvQ-qT6uZpzF/view?usp=drive_link): 訓練時的資料集檔案 (ex: .data & .name)
   - [weights](https://drive.google.com/file/d/1d8KwqC6-Fz1MZbxDRH_kDJQOipFIMCgT/view?usp=sharing): 訓練後的模型權重檔案 (ex: .weights)

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