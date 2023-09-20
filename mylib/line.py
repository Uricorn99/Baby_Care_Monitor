import requests
import datetime
from time import time


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
            print('0')
            print(detections)
            test_result = detections[0][0]
            print(test_result)
            now_time = time()
            if test_result == "Danger":
                now_alarm = time()
                print(test_result)
                if test_result == old_result:
                    print('1')
                    if now_alarm - first_alarm > kt:
                        print('2')
                        if send_time is None:
                            print('3')
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
                            print('4')
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