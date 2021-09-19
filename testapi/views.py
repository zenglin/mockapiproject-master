from rest_framework import views
from rest_framework.response import Response
from .models import *
import json,requests
from django.shortcuts import render



class initclass(object):
    '''初始化属性配置'''

    def __init__(self):
        self.code = ['code', '-1']
        self.msg = ['msg']
        self.data = ['data', None]


class Caseid(views.APIView, initclass):
    '''自定义视图/caseid查询'''

    def get(self, request, *args):
        caseid = list(args)[-1]
        try:
            db_data = CaseidMock.objects.get(Caseid=caseid)
            re_data = json.loads(db_data.ResponseData)
        except IndexError:
            msg = 'caseid表未配置{}的数据'.format(self.request.path)
            re_data = {self.code[0]: self.code[1], self.msg[0]: msg, self.data[0]: self.data[1]}
            return Response(re_data)
        return Response(re_data)

class IndexClass(object):
    def index(request):
        header = request.POST.get('header')
        url = request.POST.get('url', None)
        req_type = request.POST.get('req_type', None)
        try:
            requestsdata = json.loads(request.POST.get('requestsdata'))
        except ValueError:
            requestsdata = None
        if req_type == 'post':
            data = requests.post(url, json=requestsdata, headers=eval(header))
        elif req_type == 'get':
            data = requests.get(url)
        result = data.json()
        return render(request, "index.html", {"data": data.status_code, "data1": result})
