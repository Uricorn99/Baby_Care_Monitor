from django.shortcuts import render
from django.http import JsonResponse

global_param = {
        "acc": 0.5,
        "dangertime": 30,
        "warningtime": 2,
        "toggle_notification": 'true',
        "recording": 'false'
}

def get_param():
    return global_param


def get_data_from_request(request):
    # 从请求中获取参数
    acc = request.GET.get('acc')
    dangertime = request.GET.get('dangertime')
    warningtime = request.GET.get('warningtime')
    toggle_notification = request.GET.get('toggle_notification')
    recording = request.GET.get('recording')
    


    global_param['acc']=acc
    global_param['dangertime']=dangertime
    global_param['warningtime']=warningtime
    global_param['toggle_notification']=toggle_notification
    global_param['recording']=recording



    # 返回 JSON 响应
    response = JsonResponse(global_param, status=200)
    return response
