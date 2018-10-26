"""
index 视图
"""
from app.views import returnOk, returnBadRequest, checkPara, returnForbidden
from django.http import request
from django.http import HttpResponse
from weixin.utils import checkSignature, WeixinParser
from app.util import FileLogger
from weixin.models import Weixin, User

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

    # 如果是校验请求
    if request.method == "GET":
        echostr = request.GET.get("echostr")
        return HttpResponse(echostr)

    msgData = WeixinParser.parseXml(request.body)
    FileLogger.log_info("weixin_parse_data", msgData.__dict__, handler_name=FileLogger.WEIXIN_HANDLER)
    if msgData.msgType == "event":  # 推送事件
        if msgData.event == "subscribe" or msgData.event == "SCAN":
            FileLogger.log_info("xxxxxxxxxxxx_look_there_xxxxxxxxxxxxxx", msgData, FileLogger.WEIXIN_HANDLER)


    resData = WeixinParser.returnTextMessage(msgData.fromUserName, "你什么关注我？(羞赧)")

    return HttpResponse(resData, content_type="application/xml")



