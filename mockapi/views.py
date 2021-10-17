from rest_framework import views
from rest_framework.response import Response
from django.shortcuts import render
from mockapi.models import *
import json, requests
from defmethod.viewsmethod import Querymethod, DataCheck, Currency
from defmethod.Log import logger


class CurrencyRoute(views.APIView, Currency):
    '''通用模式下-API接口视图类'''

    def __init__(self):
        super(Currency, self).__init__()
        self.code = ['code', '-1']
        self.msg = ['msg']
        self.data = ['data', None]
        self.DataCheck = DataCheck(self.code, self.msg, self.data)
        self.response_data = {self.code[0]: self.code[1], self.msg[0]: None, self.data[0]: self.data[1]}

    # 根据url找路由表数据：路由id、条件匹配规则、字段要求规则
    def __getroute(self, args, UrlType):
        re_path = self.request.path
        # 获取后缀url路径:因url带了横杠会被切片，导致获取元素不完整。故会走另一个方法来避免
        route = "/".join(list(args)) if re_path.find('-') == -1 else self.find_path("/", re_path, args)
        get_data = RouteTabMock.objects.get(CustomUrl=route, UrlType=UrlType, APIOnOff=True)
        re_data = get_data.id, get_data.ConditionValue, get_data.APIRequired
        logger.info('路由id={},条件匹配={}，必填及类型规则={}'.format(re_data[0], re_data[1], re_data[2]))
        return re_data

    # 接口请求处理，数据处理/规则处理
    def __requestprocess(self, path_a):
        logger.info(
            '{}\n请求类型={},地址={},报文={}'.format(80 * '=', self.request.method, self.request.path, self.request.data))
        request_data = dict(self.request.GET) if self.request.method == 'GET' else dict(self.request.data)
        # 预留一个后门属性，如果有此test_data字段直接返回
        if Currency.test_data(request_data) != None:
            if self.request.method == 'GET':
                re_data = eval(request_data['test_data'][0])
            else:
                re_data = request_data['test_data']
            return re_data
        # 获取路由id、条件匹配规则、必填及数据类型规则
        try:
            re_dataid, conditionValue, apirequired = self.__getroute(path_a, UrlType=self.request.method)
        except:
            msg = '路由表未配置该url:' + self.request.path
            self.response_data[self.msg[0]] = msg
            logger.error('{},请求返回值={}'.format(msg, self.response_data))
            return self.response_data
        # 对传入参数进行必填项校验和数据类型的校验，校验不通过为False，返回Response错误的响应体
        re_data = self.DataCheck.check(eval(apirequired), request_data)
        if re_data != True:
            return re_data
        # 依据条件匹配规则，找到入参对应的条件查询值
        QueryValue = Querymethod().match_value(request_data, conditionValue, self.request.method)
        logger.info('条件匹配规则结果:' + str(QueryValue))
        # 如无条件匹配规则，取该接口下最新mock数据
        if QueryValue == False:
            try:
                getdb_data = APIResponseMock.objects.filter(CustomUrl_id=re_dataid)
                db_data = list(getdb_data.values())[-1]['ResponseData']
                re_data = json.loads(db_data)
            except IndexError:
                msg = 'mock表未配置该url{}对应的数据'.format(self.request.path)
                self.response_data[self.msg[0]] = msg
                logger.error(msg)
        # 如果有条件匹配规则，对应的匹配值；如果存在多个匹配值，取第一个匹配的mock值
        else:
            try:
                con = self.Q_model(QueryValue, re_dataid)
                getdb_data = APIResponseMock.objects.filter(con)
                db_data = list(getdb_data.values())[-1]['ResponseData']
                re_data = json.loads(db_data)
            except Exception as ex:
                msg = '未找到匹配值:' + str(QueryValue)
                re_data = {self.code[0]: self.code[1], self.msg[0]: msg, self.data[0]: self.data[1]}
                logger.error(msg)
        logger.info('请求返回值=' + str(re_data))
        return re_data

    # post请求方式
    def post(self, request, *args):
        re_data = self.__requestprocess(args)
        return Response(re_data)

    # Get请求方式
    def get(self, request, *args):
        re_data = self.__requestprocess(args)
        return Response(re_data)

    # Put请求方式
    def put(self, request, *args):
        re_data = self.__requestprocess(args)
        return Response(re_data)


class IndexClass(views.APIView):
    '''接口测试页面视图'''

    def index(request):
        status_code = result = str()
        url = 'http://'
        header = '{"Content-Type":"application/json"}'
        requedata = '{}'
        # 根据请求类型判断是提交或是获取html资源
        if request.method == 'POST':
            header = request.POST.get('header')
            url = request.POST.get('url', None)
            req_type = request.POST.get('req_type', None)
            try:
                requedata = json.loads(request.POST.get('requedata'))
            except ValueError:
                requedata = None
            if req_type == 'post':
                data = requests.post(url, json=requedata, headers=eval(header))
            elif req_type == 'get':
                data = requests.get(url, headers=eval(header))
            elif req_type == 'put':
                data = requests.put(url, json=requedata, headers=eval(header))
            status_code = data.status_code
            result = data.json()
            requedata = json.dumps(requedata)
        return render(request, 'index.html',
                      {'status_code': status_code, 'result': result, 'url': url, 'header': header,
                       'requedata': requedata})
