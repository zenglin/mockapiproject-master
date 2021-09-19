from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path('caseid/(\w+)', views.Caseid.as_view(), name='caseid'),  # 自定义路由2,url为变量
]