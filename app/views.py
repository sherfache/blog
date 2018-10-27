from django.http import JsonResponse, HttpResponse, HttpResponseRedirect

# Create your views here.

def returnBase(message="", code=1, status=400):
    data = {
        "err_code": code,
        "message":message
    }
    return JsonResponse(data, status=status)

def returnNotFound(message, code=1):
    return  returnBase(message, code)

def returnOk(data=None):
    if not data:
        data = {}
    return JsonResponse(data=data, status=200)

def returnBadRequest(message, code=1):
    return returnBase(message, code)

def returnForbidden(message, code=1):
    return returnBase(message, code, status=403)

def returnRedirect(location):
    return HttpResponseRedirect(location)

# 检查参数
def checkPara(dataMap, keyList):
    if not isinstance(dataMap, dict) or not isinstance(keyList, list):
        return False

    result = [True]
    for k in keyList:
        if k not in dataMap:
            if result[0] == True:
                result[0] = "Need para: " + k
            value = None
        else:
            value = dataMap[k]
        result.append(value)

    return tuple(result)
