from datetime import datetime
from django.conf import settings
import logging
from logging.handlers import TimedRotatingFileHandler

class Date:

    # %Y-%m-%d
    @staticmethod
    def date(dt=None):
        if dt:
           try:
               return dt.strftime("%Y-%m-%d")
           except:
               return None
        else:
            return datetime.now().strftime("%Y-%m-%d")

    # %Y-%m-%d %H:%M:%S
    @staticmethod
    def datetime(dt=None):
        if dt:
            try:
                return dt.strftime("%Y-%m-%d %H:%M:%S")
            except:
                return None
        else:
            return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class Auth:

    @staticmethod
    def checkOperator(request):
        operator = request.POST.get("operator", None)
        password = request.POST.get("password", None)
        authMap = settings.OPERATOR_AUTH
        if operator not in authMap:
            return False
        if authMap[operator] == password:
            return True
        return False


# 文件日志
class FileLogger:
    """
    日志文件
    """

    # 文件日志handler名
    COMMON_HANDLER = "common_handler"  # 通用日志
    WEIXIN_HANDLER = "weixin_handler"  # 微信日志
    IMAGE_HANDLER = "image_handler"  # 图片日志

    # 通用格式
    g_formatter = logging.Formatter(
        fmt="%(name)s - %(asctime)s - %(levelname)s : %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S")
    # 日志处理器配置
    handler_config_dict = {
        COMMON_HANDLER: {
            'filename': 'common.log',  # 文件名
            'when': 'D',  # 翻转间隔类型
            'interval': 7,  # 翻转间隔
            'backupCount': 4  # 备份数
        },
        WEIXIN_HANDLER: {
            'filename': 'weixin.log',  # 文件名
            'when': 'D',  # 翻转间隔类型
            'interval': 7,  # 翻转间隔
            'backupCount': 4  # 备份数
        },
        IMAGE_HANDLER: {
            'filename': 'image.log',  # 文件名
            'when': 'D',  # 翻转间隔类型
            'interval': 7,  # 翻转间隔
            'backupCount': 4  # 备份数
        },
    }

    @classmethod
    def get_logger(cls, handler_name=COMMON_HANDLER):
        """
        根据handler名 获取不同的logger
        :return:
        """
        logger = logging.getLogger(handler_name)
        if not logger.handlers:
            formatter = cls.g_formatter
            logger.setLevel(logging.INFO)
            handler_config = cls.handler_config_dict[handler_name]
            handler = TimedRotatingFileHandler(filename=settings.BASE_DIR + "/logs/" + handler_config['filename'],
                                               when=handler_config['when'],
                                               interval=handler_config['interval'],
                                               backupCount=handler_config['backupCount'])
            handler.setFormatter(formatter)
            handler.suffix = "%Y-%m-%d_%H-%M-%S.log"
            logger.addHandler(handler)
        return logger

    @classmethod
    def log_info(cls, log_type, message="", handler_name=COMMON_HANDLER):
        """
        记录日志 - info 级别
        :param logType: 自定义的标志字符串 - 操作类型
        :param message:
        :return:
        """
        logger = cls.get_logger(handler_name)
        try:
            message = str(message)
            log_type = str(log_type)
        except Exception as e:
            message = e
            log_type = "logging-error"
        msg = " %s - %s " % (log_type, message)
        logger.info(msg.encode("utf8"))

    @staticmethod
    def dict2str(key_list, data_dict):
        """
        根据key_list 将字典转拼接成字符串 - 方便阅读
        :param key_list:
        :param data_dict:
        :return:
        """
        if not isinstance(key_list, list) and not isinstance(data_dict, dict):
            return ""
        result = ""
        sperator = " - "
        for key in key_list:
            val = data_dict.get(key, "")
            result += sperator + str(key) + ":" + str(val)







