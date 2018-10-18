"""
index 视图
"""
from app.views import returnOk, returnBadRequest, checkPara, returnForbidden
from django.http import request
from django.http import HttpResponse
from weixin.utils import checkSignature
from app.util import FileLogger

# 推送入口
def index(request):
    # 校验合法性
    result, signature, timestamp, nonce = checkPara(request.GET, [
        "signature", "timestamp", "nonce"
    ])
    if result != True:
        return returnBadRequest(result)

    if not checkSignature(signature, timestamp, nonce):
        return returnForbidden("Fuck off.")

    FileLogger.log_info("weixin_data", request.GET, handler_name=FileLogger.WEIXIN_HANDLER)

    # 如果是校验请求
    if request.method == "GET":
        echostr = request.GET.get("echostr")
        return HttpResponse(echostr)

    # 记录文件日志
    FileLogger.log_info("weixin_data", request.POST, handler_name=FileLogger.WEIXIN_HANDLER)

    return returnOk()

