from django.urls import path, re_path
from . import views

urlpatterns = [
    path(r'index', views.IndexClass.index, name='index-test')  # 接口测试页面
]
add_path = [
    re_path(r'(\w+)/(\w+)/(\w+)', views.CurrencyRoute.as_view(), name='test3-api-viewstwo'),  # 动态路由+3
    re_path(r'(\w+)/(\w+)', views.CurrencyRoute.as_view(), name='test2-api-viewstwo'),  # 动态路由+2
    re_path(r'(\w+)', views.CurrencyRoute.as_view(), name='test1-api-viewstwo'),  # 动态路由+1
]
urlpatterns.extend(add_path)
