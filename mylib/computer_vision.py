import cv2
import os
import random
import time
    
def select_random_image_from_folder(path:str) -> cv2.Mat:
    '''
    從資料夾中選擇隨機圖像

    parameters:

    path: 資料夾路徑

    return:

    圖像
    '''
    if not os.path.exists(path):
        raise ('資料夾路徑錯誤!')

    test_images = [f for f in os.listdir(path) if f.endswith('.jpg')]

    # 隨機圖像路徑
    return cv2.imread(path + random.choice(test_images))

def draw_obj_rec(img:cv2.Mat, class_name:str, score:float, box:list, color:tuple=(0,255,0)):
    '''
    繪製物件的外框、分類名稱與信任分數

    parameters:
    
    img: 圖像

    class_name: 分類名稱

    score: 信任分數

    box: 物件外框

    color: 外框與文字顏色
    '''
    # 繪製矩形
    x,y,w,h=box[0],box[1],box[2],box[3]
    cv2.rectangle(img, (x, y), (x + w, y + h), color, 3)    # 圖片, 起點, 終點, 顏色, 線粗
    
    # 繪製類別與信任分數
    text = f"{class_name} {round(score * 100, 2)}%"
    y = y - 10 if y - 10 > 10 else y + 15
    cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)

    return img

def cam_init(index:int=0, is_write:bool=False,save_path:str=None) -> tuple:
    '''
    攝影機

    parameters:

    index: cam

    is_write: 是否儲存影像檔案

    save_path: 影像檔案路徑

    return:

    cap:攝影機物件, writer:影像寫入物件, height:影像高, width:影像寬
    '''
    writer = None
    cap = cv2.VideoCapture(index)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)#default 480
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)#default 640

    if is_write:
        fourcc = cv2.VideoWriter_fourcc(*'divx')
        if save_path is None:
            save_path = 'demo.avi'
        writer = cv2.VideoWriter(save_path, fourcc, 30, (int(width), int(height)))

    return cap,writer,height,width

def calc_fps(start_time:float):
        '''
        FPS calculation

        Parameters:

        start_time:紀錄起始時間

        Return:

        FPS
        '''
        fps = int(1/(time.time()-start_time))
        return fps