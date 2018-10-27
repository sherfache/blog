from django.urls import path
from weixin import index
from django.conf import settings


# 微信公众号后台提供的url
weixin_patterns = [
    path("/", index.index),

]

if settings.DEBUG:
    from weixin import localtest
    weixin_patterns.append(path("/test", localtest.test))


