"""
管理员操作
"""

from django.http import request
from app.models import Blog
from app.views import returnOk, returnNotFound, checkPara, returnBadRequest
from django.views.decorators.http import require_http_methods
from app.util import Auth


# 创建博客的接口
@require_http_methods(["POST"])
def createBlog(request):
    if not Auth.checkOperator(request):
        return returnBadRequest("权限校验失败")

    result, title, content = checkPara(request.POST, [
        "title", "content"
    ])
    if result != True:
        return returnBadRequest(result)

    blog = Blog(
        title=title,
        content=content
    )
    blog.save()

    return returnOk()


# 更新博客的接口
@require_http_methods(["POST"])
def updateBlog(request):
    if not Auth.checkOperator(request):
        return returnBadRequest("权限校验失败")

    result, blogId, title, content = checkPara(request.POST, [
        "blogId", "title", "content"
    ])
    if result != True:
        return returnBadRequest(result)

    blog = Blog.getBlogById(blogId)
    if not blog:
        return returnBadRequest("博客不存在")

    blog.title = title
    blog.content = content
    blog.save()

    return returnOk()





































