import requests
import datetime
from time import time
import threading
import queue

class Notify:
    def __init__(self):
        """
        Line Notify\n
        detections (list): 物件偵測回傳的list\n
        kt (float): 姿勢維持多久觸發警報\n
        imageFile (dict): 危險姿勢截圖\n
        si (float): 警報間隔
        token (str): line通知令牌  
        """
        self.q = queue.Queue()
        # self.q1 = queue.Queue()
        self.send_time = None
        self.send = 'No'
        self.old_result = None
        self.first_alarm = None
        self.data = None
    # 發通知
    def send_work(self, data, imageFile):
        while True:
            task = self.q.get()

            url = "https://notify-api.line.me/api/notify"
            token = "HYqb8GwjgljZ5fU2uxMhnC8zewF6TNJci8Z65GPDybv"
            headers = {'Authorization': 'Bearer ' + token}

            try:
                if task:
                    respon = requests.post(url, headers=headers, data=task[0], files=task[1])
                    print(f'Working')
                    # print(f'響應內容：{respon.text}')
                    # print(f'{respon} is finished')
                    # self.send_time = time()
                    # self.q1.put(send_time)
            except Exception as e:
                print("An error occurred:", str(e))
            finally:
                print('Send_Done')
                self.q.task_done()
                
    # def get_send_time(self):
    #     try:
    #         if self.send == 'Yes':
    #             return self.q1.get()
    #         else:
    #             return None
    #     except Exception as e:
    #             print("An error occurred:", str(e))
    #     return None
        
    def line_notify(self, detections, kt, si, tn):
        if tn == "true":
            try:
                test_result = detections[0][0]
                now_time = time()
                if test_result == "Danger":
                    now_alarm = time()
                    if test_result == self.old_result:
                        if now_alarm - self.first_alarm > kt:
                            # print('超過持續時間了')
                            # print(self.send_time)
                            # print(si)
                            # if self.send_time is not None:
                            #     print(now_alarm - self.send_time)
                            if self.send_time is None:
                                print('發第一次通知')
                                now = datetime.datetime.now()
                                formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
                                self.data = {
                                    "message": f'Warning: Your baby is at risk!\n'
                                            f'姿勢維持時間:{round(now_alarm - self.first_alarm)}秒鐘\n'
                                            f'現在時間:{formatted_time}'                                    
                                }
                                self.send = 'Yes'
                                self.send_time = time()
                            elif now_alarm - self.send_time > si:
                                print('第n次通知')
                                now = datetime.datetime.now()
                                formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")                           
                                self.data = {
                                    "message": f'Warning: Your baby is at risk!\n'
                                            f'姿勢維持時間:{round(now_alarm - self.first_alarm)}秒鐘\n'
                                            f'現在時間:{formatted_time}'                                    
                                }
                                self.send = 'Yes'
                                self.send_time = time()
                        else:
                            print('翻過去了，持續時間還沒到')
                            self.old_result = test_result
                            self.send = 'No'
                            self.data = None
                    else:
                        print('剛翻過去，還不用通知')
                        self.old_result = test_result
                        self.first_alarm = now_time
                        self.send = 'No'
                        self.data = None
                else:
                    self.old_result = test_result
                    self.send = 'No'
                    self.data = None
                    print("Your baby is fine")
            except:
                self.old_result = None
                self.first_alarm = None
                self.send = 'No'
                self.data = None
                print("Baby probably not here")
        else:
            print("Notifications are not turned on")
            self.old_result = None
            self.first_alarm = None
            self.send = 'No'
            self.data = None