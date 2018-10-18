"""
工具类
"""
from django.conf import settings
import hashlib


# 微信签名验证方法
def checkSignature(signature, timestamp, nonce):
    token = settings.WEIXIN_OPEN_TOKEN
    tmpArr = [token, timestamp, nonce]
    tmpArr.sort()
    strTmp = tmpArr[0] + tmpArr[1] + tmpArr[2]
    sigLoc = hashlib.sha1(strTmp).hexdigest()
    if sigLoc == signature:
        return True
    return False


