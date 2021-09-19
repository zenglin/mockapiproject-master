from django.db import models
from django.core.exceptions import ValidationError
import json


class CaseidMock(models.Model):
    """自定义模型/caseid 查询"""

    Caseid = models.CharField(max_length=30, db_index=True, unique=True, verbose_name='Caseid')
    UpdateTime = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    ResponseData = models.TextField(verbose_name='响应信息数据')

    def clean(self):
        try:
            json.loads(self.ResponseData)
        except json.JSONDecodeError:
            raise ValidationError('响应信息json数据不合法，请检查')

    class Meta:
        verbose_name = 'caseid / 查询'
        verbose_name_plural = 'caseid / 查询'

    def __str__(self):
        return ' Caseid: {caseid} - - 更新时间:{UpdateTime} '.format(UpdateTime=str(self.UpdateTime)[:19],caseid=self.Caseid)
