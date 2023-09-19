from django.shortcuts import render
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
