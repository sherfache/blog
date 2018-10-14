from django.http import request, JsonResponse
from django.shortcuts import render
from app.models import Blog
from app.views import returnNotFound, returnOk
import markdown
from app.util import Date


# 首页视图
def index(request):
    blogs = Blog.getAllBlog()
    return render(request, "blog/index.html", context={"blogList":blogs})


# 获取详情的视图
def detail(request, blogId):
    blog = Blog.getBlogById(blogId)
    if not blog:
        return returnNotFound()
    # 自增pv
    blog.increaseViews()
    blog.content = markdown.markdown(blog.content,
                                     extensions=[
                                         "markdown.extensions.extra",
                                         "markdown.extensions.codehilite",
                                         "markdown.extensions.toc"
                                     ])
    return render(request, "blog/detail.html", context={"blog":blog})


