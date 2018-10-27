## 博客url
from django.urls import path
from app import index, admin, upload_views


app_name = "app"
blog_patterns = [
    path("", index.index),
    path("article/<int:blogId>", index.detail, name="detail"),

    # 管理接口
    path("admin/createBlog", admin.createBlog),
    path("admin/updateBlog", admin.updateBlog),

    # 上传图片的接口
    path("upload/image", upload_views.uploadImage),


]




