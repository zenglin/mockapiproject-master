# Generated by Django 2.2.6 on 2021-09-16 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testapi', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='caseidmock',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
