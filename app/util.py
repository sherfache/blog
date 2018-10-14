from datetime import datetime
from django.conf import settings

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




if __name__ == "__main__":
    print(Date.datetime())












