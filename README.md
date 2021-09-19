
### 系统说明


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

