# 標題待定

## Requirement

- Python 3.7.16
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

## Folder

- cfg: 模型參數 (ex: yolo-obj.cfg)
- data: 訓練時的資料集檔案 (ex: obj.data & obj.name)
- weights: 訓練後的模型權重檔案 (ex: yolo-obj.weights)
- yolo: darknet 原作者的函式庫

## Usage

- Run server

```bash
python manage.py runserver
```
