from django.urls import path
from weixin import index

# 微信公众号后台提供的url
weixin_patterns = [
    path("/", index.index),

]







