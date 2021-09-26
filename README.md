
### 背景说明

因在版本迭代过程中，一般都需要调用接口来实现需求业务。而前后端或各系统之间都存在强依赖性，故构思了此Mock接口。主要解决如下场景：
  
  1、前后端的依赖关系：如前端已开发完毕但后端还没完成，导致前端无法进行调试;
  
  2、外部系统依赖关系：如外部系统未开发完或者环境的因素无法完成对接调试;
  
  3、测试阶段依赖关系：测试的某些场景无法模拟下，可调用mock接口设置自定义返回值，从而达到测试场景的覆盖(主要就是这块，因咱就是干测试滴)；

### 关键文件/文件夹说明

data/: 存放数据文件，系统存储采用sqlite3

defmethod/:存放需调用的方法

mockproject/settings.py: 系统配置文件

mockproject/urls.py: 总路由

mockapi/urls.py: mock模块子路由

mockapi/models.py: mock模块模型

mockapi/views.py: mock模块视图




### 部署

系统部署需要`python3.0`以上环境，


确保 data 目录存在

```shell
mkdir data
```

首次启动，需要执行
```shell
python manage.py migrate
```

启动：

`python manage.py runserver`

## 创建超级用户

```
python manage.py createsuperuser
```

## 添加模型之后，自动创建 migrations

```
# 自动创建 migrations
python manage.py makemigrations

# 应用 migration
python manage.py migrate
```

