from django.shortcuts import render

# Create your views here.

from django.http import JsonResponse

def test(request):
    # 从请求中获取参数
    param_a = request.GET.get('param_a')
    param_b = request.GET.get('param_b')
    param_c = request.GET.get('param_c')
    toggle_notification = request.GET.get('toggle_notification')
    toggle_image = request.GET.get('toggle_image')

    # 构建要返回的数据
    data = {
        "param_a": param_a,
        "param_b": param_b,
        "param_c": param_c,
        "toggle_notification": toggle_notification,
        "toggle_image": toggle_image,
    }

    # 返回 JSON 响应
    response = JsonResponse(data, status=200)
    return response