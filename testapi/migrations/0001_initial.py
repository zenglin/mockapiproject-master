# Generated by Django 3.2.6 on 2021-09-12 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CaseidMock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Caseid', models.CharField(db_index=True, max_length=30, unique=True, verbose_name='Caseid')),
                ('UpdateTime', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('ResponseData', models.TextField(verbose_name='响应信息数据')),
            ],
            options={
                'verbose_name': 'caseid / 查询',
                'verbose_name_plural': 'caseid / 查询',
            },
        ),
    ]
