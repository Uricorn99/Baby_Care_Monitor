import requests
import datetime
from django.shortcuts import render
from time import time
from django.http import JsonResponse

global_param = {
        "acc": 0.5,
        "dangertime": 5,
        "warningtime": 5,
        "toggle_notification": False,        
}
def get_param():
    return global_param

def test(request):
    # 从请求中获取参数
    param_a = request.GET.get('param_a')
    param_b = request.GET.get('param_b')
    param_c = request.GET.get('param_c')
    toggle_notification = request.GET.get('toggle_notification')

    # 构建要返回的数据
    global_param["acc"] = param_a
    global_param["dangertime"] = param_b
    global_param["warningtime"] = param_c
    global_param["toggle_notification"] = toggle_notification

    # 返回 JSON 响应
    response = JsonResponse(global_param, status=200)
    return response

def line_notify(tn,detections,kt,imageFile,si):
    """
    Line Notify\n
    tn (str): 是否開啟通知\n
    detections (list): 物件偵測回傳的list\n
    kt (float): 姿勢維持多久觸發警報\n
    imageFile (dict): 危險姿勢截圖\n
    si (float): 警報間隔
    token (str): line通知令牌  
    """
    url = "https://notify-api.line.me/api/notify"
    token = "ubJnBPx5JLWX5FqXLmfIxmUUsxfFcCE402PlICSJeNi"
    headers = {'Authorization': 'Bearer ' + token}
    global old_result 
    global first_alarm
    global send_time    
    if tn == "true":
        try:
            test_result = detections[0][0]
            now_time = time()
            if test_result == "Danger":
                now_alarm = time()              
                if test_result == old_result:
                    if now_alarm - first_alarm > kt:                             
                        if send_time is None:
                            now = datetime.datetime.now()
                            formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
                            data = {
                                "message": f'Warning: Your baby is at risk!\n'
                                           f'姿勢維持時間:{now_alarm - first_alarm}\n'
                                           f'現在時間:{formatted_time}'                                    
                            }
                            respon = requests.post(url, headers=headers, data=data, files=imageFile)
                            #print(respon.status_code)    
                            send_time = time() 
                        elif now_alarm - send_time > si:
                            now = datetime.datetime.now()
                            formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")                           
                            data = {
                                "message": f'Warning: Your baby is at risk!\n'
                                           f'姿勢維持時間:{now_alarm - first_alarm}\n'
                                           f'現在時間:{formatted_time}'                                    
                            }
                            respon = requests.post(url, headers=headers, data=data, files=imageFile)                        
                            send_time = time()
                else:
                    old_result = test_result
                    first_alarm = now_time                           
                    send_time = None         
            else:
                old_result = test_result
                send_time = None
                print("Your baby is fine")                
        except:
            print("Baby probably not here")
    else:            
        old_result = None
        first_alarm = None
        send_time = None
    return old_result, first_alarm, send_time
