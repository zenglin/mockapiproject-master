from django.contrib import admin
from .models import *


class RouteTabMockAdmin(admin.ModelAdmin):

    def time_seconds(self, obj):
        return obj.UpdateTime.strftime("%Y-%m-%d %H:%M:%S")

    # 时间格式化处理
    time_seconds.admin_order_field = 'UpdateTime'
    time_seconds.short_description = '更新时间'
    list_display = ['id', 'UrlName', 'CustomUrl', 'UrlType', 'apirequired', 'routeprofile', 'time_seconds',
                    'APIOnOff', ]
    list_filter = ['CustomUrl']
    search_fields = ['CustomUrl']
    list_per_page = 10
    actions_on_top = False
    actions_on_bottom = True
    fieldsets = [
        ("接口信息", {"fields": ['UrlName', 'CustomUrl', 'UrlType']}),
        ("接口规则", {"fields": ['APIOnOff', 'APIRequired', 'ConditionValue']})
    ]

admin.site.register(RouteTabMock, RouteTabMockAdmin)


@admin.register(APIResponseMock)
class APIResponseMockAdmin(admin.ModelAdmin):
    def time_seconds(self, obj):
        return obj.UpdateTime.strftime("%Y-%m-%d %H:%M:%S")

    # 时间格式化处理
    time_seconds.admin_order_field = 'UpdateTime'
    time_seconds.short_description = '更新时间'
    list_display = ['id', 'CustomUrl', 'QueryValue', 'reprofile', 'time_seconds','Remarks']
    list_filter = ['CustomUrl']
    search_fields = ['CustomUrl__CustomUrl']
    # 执行动作的位置
    actions_on_top = False
    actions_on_bottom = True

class IndexClassAdmin(admin.ModelAdmin):
    pass
admin.site.register(index, IndexClassAdmin)

