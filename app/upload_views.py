"""
文件上传视图
"""
from django.views.decorators.http import require_http_methods
import filetype, hashlib
from app.views import returnOk, returnForbidden, returnBadRequest
from app.models import UploadImage
from app.util import FileLogger, Auth
from django.conf import settings

# 上传文件的视图
@require_http_methods(["POST"])
def uploadImage(request):
    if not Auth.checkOperator(request):
        return returnForbidden("无权限")

    file = request.FILES.get("img", None)
    if not file:
        return returnBadRequest("need file.")

    # 图片大小限制
    if not pIsAllowedFileSize(file.size):
        return returnForbidden("文件太大")

    # 计算文件md5
    md5 = pCalculateMd5(file)
    uploadImg = UploadImage.getImageByMd5(md5)
    if uploadImg:   # 文件已存在
        return returnOk({'url': uploadImg.getImageUrl()})

    # 获取扩展类型 并 判断
    ext = pGetFileExtension(file)
    if not pIsAllowedImageType(ext):
        return returnForbidden("文件类型错误")

    # 检测通过 创建新的image对象
    uploadImg = UploadImage()
    uploadImg.filename = file.name
    uploadImg.file_size = file.size
    uploadImg.file_md5 = md5
    uploadImg.file_type = ext
    uploadImg.save()

    # 保存 文件到磁盘
    with open(uploadImg.getImagePath(), "wb+") as f:
        # 分块写入
        for chunk in file.chunks():
            f.write(chunk)

    # 文件日志
    FileLogger.log_info("upload_image", uploadImg, FileLogger.IMAGE_HANDLER)

    return returnOk({"url": uploadImg.getImageUrl()})



# 检测文件类型
def pGetFileExtension(file):
    rawData = bytearray()
    for c in file.chunks():
        rawData += c
    try:
        ext = filetype.guess_extension(rawData)
        return ext
    except Exception as e:
        # todo log
        return None


# 计算文件的md5
def pCalculateMd5(file):
    md5Obj = hashlib.md5()
    for chunk in file.chunks():
        md5Obj.update(chunk)
    return md5Obj.hexdigest()


# 文件类型过滤
def pIsAllowedImageType(ext):
    if ext in ["png", "jpeg", "jpg"]:
        return True
    return False

# 文件大小限制
def pIsAllowedFileSize(size):
    limit = settings.IMAGE_SIZE_LIMIT
    if size < limit:
        return True
    return False




























