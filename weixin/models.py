from django.db import models
from django.conf import settings
import requests
from app.util import FileLogger
import datetime

# Create your models here.

# 微信数据&接口操作模型
class Weixin:

    accessToken = None
    expire_at = datetime.datetime.now()

    # 获取用户信息
    @classmethod
    def getUserInfo(cls, openId):
        url = "https://api.weixin.qq.com/cgi-bin/user/info"
        para = {
            "access_token": cls.getAccessToken(),
            "openid": openId,
            "land": "zh_CN"
        }
        try:
            res = requests.get(url, para).json()
            FileLogger.log_info("user_info", res, handler_name=FileLogger.WEIXIN_HANDLER)
            return res
        except Exception as e:
            FileLogger.log_info("request_error", e, handler_name=FileLogger.WEIXIN_HANDLER)
            return None

    @classmethod
    def requestAccessToken(cls):
        url = "https://api.weixin.qq.com/cgi-bin/token"
        para = {
            "grant_type": "client_credential",
            "appid": settings.WEIXIN_APP_ID,
            "secret": settings.WEIXIN_APP_SECRET
        }
        try:
            res = requests.get(url, para).json()
            FileLogger.log_info("access_token", res, handler_name=FileLogger.WEIXIN_HANDLER)
            cls.accessToken = res["access_token"]
            cls.expire_at = datetime.datetime.now() + datetime.timedelta(seconds=res["expires_in"]-600)
            return res["access_token"]
        except Exception as e:
            FileLogger.log_info("request_error", e, handler_name=FileLogger.WEIXIN_HANDLER)
            return None

    @classmethod
    def getAccessToken(cls):
        if not cls.accessToken or cls.expire_at < datetime.datetime.now():
            return cls.requestAccessToken()
        return cls.accessToken

# 用户信息模型
class User(models.Model):

    db_table = "user"

    openid = models.CharField(max_length=128, primary_key=True)
    nickname = models.CharField(max_length=128)
    sex = models.IntegerField(default=0)
    country = models.CharField(max_length=32)
    province =models.CharField(max_length=32)
    city = models.CharField(max_length=64)
    headimgurl = models.CharField(max_length=2040)
    subscribe_time = models.DateTimeField(default=datetime.datetime.now)
    created_at = models.DateTimeField(default=datetime.datetime.now)
    updated_at = models.DateTimeField(default=datetime.datetime.now)


    @staticmethod
    def getUser(id):
        try:
            if not id:
                return None
            return User.objects.get(openid=id)
        except Exception as e:
            return None

    # create & update
    @staticmethod
    def saveUser(data):
        try:
            if isinstance(data, dict):
                return None
            user = User.getUser(data.get("openid"))
            if not user:
                user = User(openid=data["openid"])
            user.nickname = data.get("nickname", "")
            user.sex = data.get("sex", 0)
            user.country = data.get("country", "")
            user.province = data.get("province", "")
            user.city = data.get("city", "")
            user.headimgurl = data.get("headimgurl", "")
            user.subscribe_time = data.get("subscribe_time", datetime.datetime.now())
            user.save()
            return user
        except Exception as e:
            return None


































