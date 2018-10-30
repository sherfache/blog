from django.db import models
from datetime import datetime
from django.urls import reverse
import markdown
from django.utils.html import strip_tags
from app.util import Date
from django.conf import settings


class Category(models.Model):
    class Meta:
        db_table = "category"

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=128)
    blog_num = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(default=datetime.now)


class Blog(models.Model):
    class Meta:
        db_table = "blog"

    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=512)
    content = models.TextField(default="")
    digest = models.TextField(default="")
    author = models.TextField(default="帅番茄")
    category_id = models.IntegerField(default=0)
    words_num = models.IntegerField(default=0)
    blog_status = models.IntegerField(default=1)
    view_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(default=datetime.now)


    class BlogStatus:
        ON_LINE = 1  # 上线
        OFF_LINE = 2  # 下线

    def __str__(self):
        return self.title

    # 重载save方法
    def save(self, *args, **kwargs):
        # 如果没有填写摘要
        if not self.digest:
            md = markdown.Markdown(extensions=[
                "markdown.extensions.extra",
                "markdown.extensions.codehilite",
            ])
            self.digest = strip_tags(md.convert(self.content))[:84] + "..."
        super(Blog, self).save(*args, **kwargs)

    # 通过blogId获取博客
    @classmethod
    def getBlogById(cls, blogId):
        try:
            return Blog.objects.get(id=blogId)
        except:
            return None

    # 获取博客文章的url
    def getAbsoluteUrl(self):
        return reverse("detail", kwargs={"blogId": self.id})

    # 获取所有的博客
    @classmethod
    def getAllBlog(cls):
        try:
            return Blog.objects.all().order_by("-id")
        except:
            return None

    # 自增pv
    def increaseViews(self):
        self.view_count += 1
        self.save(update_fields=["view_count"])

    # 获取格式化的日期
    def getDate(self):
        return Date.date(self.created_at)


class BlogKeyword(models.Model):
    class Meta:
        db_table = "blog_keyword"

    id = models.IntegerField(primary_key=True)
    blog_id = models.IntegerField()
    keyword = models.CharField(max_length=64)
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(default=datetime.now)


class UploadImage(models.Model):
    class Meta:
        db_table = "upload_image"

    id = models.IntegerField(primary_key=True)
    filename = models.CharField(max_length=252, default="")
    file_md5 = models.CharField(max_length=128)
    file_type = models.CharField(max_length=32)
    file_size = models.IntegerField()
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(default=datetime.now)


    @classmethod
    def getImageByMd5(cls, md5):
        try:
            return UploadImage.objects.filter(file_md5=md5).first()
        except Exception as e:
            return None

    # 获取本图片的url
    def getImageUrl(self):
        filename = self.file_md5 + "." + self.file_type
        url = settings.WEB_HOST_NAME + settings.WEB_IMAGE_SERVER_PATH + filename
        return url

    # 获取本图片在本地的位置
    def getImagePath(self):
        filename = self.file_md5 + "." + self.file_type
        path = settings.IMAGE_SAVING_PATH + filename
        return path

    def __str__(self):
        s = "filename:" + str(self.filename) + " - " + "filetype:" + str(self.file_type) \
        + " - " +  "filesize:" + str(self.file_size) + " - " + "filemd5:" + str(self.file_md5)
        return s






















