from django.db import models
from django.core.exceptions import ValidationError
from defmethod.modelsmethod import models_fun
import json


class RouteTabMock(models.Model):
    """
    Mock-路由URL表模型
    """
    ret_data = True
    re_type = [("POST", "Post"), ("GET", "Get")]
    APIOnOff = models.BooleanField(default=True, verbose_name='接口启用状态')
    UrlType = models.CharField(max_length=6, choices=re_type, default="Post", verbose_name='请求方式')
    UrlName = models.CharField(max_length=20, db_index=True, unique=True, verbose_name='接口名称')
    CustomUrl = models.CharField(max_length=50, db_index=True, unique=True, verbose_name='url地址')
    UpdateTime = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    ConditionValue = models.TextField(default='{}', verbose_name='条件匹配规则')
    APIRequired = models.TextField(default='{}', verbose_name='字段要求规则')

    class Meta:
        verbose_name = 'Mock/路由配置表'
        verbose_name_plural = 'Mock/路由配置表'

    # json格式校验，避免输入错误格式:字段要求规则、条件匹配规则
    def clean(self):
        try:
            json_data = '字段要求规则'
            json.loads(self.APIRequired)
            for key_data in str(self.ConditionValue).split(";"):
                json_data = '条件匹配规则'
                json.loads(key_data)
        except json.JSONDecodeError as ex:
            raise ValidationError('[ {} ]输入的json数据不合法，请检查.'.format(json_data))

    # 列表宽度显示限制,限制字段显示长度
    def routeprofile(self):
        re_data = models_fun().list_setting(self.ConditionValue)
        return re_data

    routeprofile.allow_tage = True
    routeprofile.short_description = '条件匹配规则'

    def apirequired(self):
        re_data = models_fun().list_setting(self.APIRequired)
        return re_data

    apirequired.allow_tage = True
    apirequired.short_description = '字段要求规则'

    def __str__(self):
        return '{}:[{}]'.format(self.UrlName, self.CustomUrl)


class APIResponseMock(models.Model):
    """
    Mock-接口数据响应表模型
    """
    CustomUrl = models.ForeignKey(RouteTabMock, on_delete=models.PROTECT, verbose_name='关联接口')
    UpdateTime = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    QueryValue = models.CharField(max_length=50, db_index=True,verbose_name='查询值')
    ResponseData = models.TextField(verbose_name='响应信息数据')

    def clean(self):
        try:
            json.loads(self.ResponseData)
        except json.JSONDecodeError:
            raise ValidationError('输入的json数据不合法，请检查')

    class Meta:
        unique_together = ('CustomUrl', 'QueryValue',)
        verbose_name = 'Mock/接口响应数据表'
        verbose_name_plural = 'Mock/接口响应数据表'

    def reprofile(self):
        re_data = models_fun().list_setting(self.ResponseData, intdata=30)
        return re_data

    reprofile.allow_tage = True
    reprofile.short_description = '响应信息数据'

    def __str__(self):
        return 'id:{}  路径:[ {} ] - 更新时间:{}'.format(self.id, self.CustomUrl, str(self.UpdateTime)[:19])

class index(models.Model):
    """
    Mock-接口数据响应表模型
    """
    class Meta:
        verbose_name = '接口测试页面'
        verbose_name_plural = '接口测试页面'