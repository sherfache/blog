"""
工具类
"""
from django.conf import settings
import hashlib
from xml.etree import ElementTree

# 微信签名验证方法
def checkSignature(signature, timestamp, nonce):
    token = settings.WEIXIN_OPEN_TOKEN
    tmpArr = [token, timestamp, nonce]
    tmpArr.sort()
    strTmp = tmpArr[0] + tmpArr[1] + tmpArr[2]
    sigLoc = hashlib.sha1(strTmp.encode("utf8")).hexdigest()
    if sigLoc == signature:
        return True
    return False


# 解析微信xml消息
class WeixinParser:

    @classmethod
    def parseXml(cls, data):
        if len(data) == 0:
            return None
        xmlData = ElementTree.fromstring(data)
        msgType = xmlData.find("MsgType").text
        if msgType == "event":
            return cls.EventMsg(xmlData)
        elif msgType == "text":
            return cls.TextMsg(xmlData)
        else:
            return cls.Msg(xmlData)


    class Msg(object):
        def __init__(self, xmlData):
            self.toUserName = xmlData.find("ToUserName").text
            self.fromUserName = xmlData.find("FromUserName").text
            self.createTime = xmlData.find("CreateTime").text
            self.msgType = xmlData.find("MsgType").text

    class EventMsg(Msg):

        def __init__(self, xmlData):
            super().__init__(xmlData)
            self.event = xmlData.find("Event").text

    class TextMsg(Msg):

        def __init__(self, xmlData):
            super().__init__(xmlData)
            self.content = xmlData.find("Content").text.encode("utf-8")
            self.msgId = xmlData.find("MsgId").text








