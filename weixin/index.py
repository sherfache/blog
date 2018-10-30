"""
index 视图
"""
from app.views import returnOk, returnBadRequest, checkPara, returnForbidden
from django.http import request
from django.http import HttpResponse
from weixin.utils import checkSignature, WeixinParser
from app.util import FileLogger
from weixin.models import Weixin
from django.conf import settings
import requests

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
            if msgData.event == "subscribe":
                sceneId = str(msgData.eventKey).split("_")[1]
            else:
                sceneId = str(msgData.eventKey)

            FileLogger.log_info("xxxxxxxxxxxx_look_there_xxxxxxxxxxxxxx", msgData, FileLogger.WEIXIN_HANDLER)
            # 拉取用户信息
            res = Weixin.getUserInfo(msgData.fromUserName)
            res.update({"sceneId": sceneId})
            # 推送用户信息
            pPushDataToAccountCenter(res)
            FileLogger.log_info("push_data", res, FileLogger.WEIXIN_HANDLER)

    resData = WeixinParser.returnTextMessage(msgData.fromUserName, "你什么关注我？(羞赧)")

    return HttpResponse(resData, content_type="application/xml")


# 推送数据
def pPushDataToAccountCenter(data):
    url = settings.YOUCLOUD_ACCOUNT_CENTER_HOST + "/weixin/data_push"
    para = {
        "sceneId": data["sceneId"],
        "unionId": data["unionid"],
        "nickname": data.get("nickname", ""),
        "headImgUrl": data.get("headimgurl", ""),
        "country": data.get("country", ""),
        "province": data.get("province", ""),
        "city": data.get("city", ""),
        "sex": data.get("sex", "0")
    }
    try :
        res = requests.post(url, json=para).json()
        FileLogger.log_info("push_to_center", res, FileLogger.WEIXIN_HANDLER)
    except Exception as e:
        FileLogger.log_info("error", e, FileLogger.WEIXIN_HANDLER)

















