# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-10-31 08:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0018_auto_20171030_2253'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='name',
            field=models.CharField(max_length=200, verbose_name='文件名称'),
        ),
        migrations.AlterField(
            model_name='function',
            name='name',
            field=models.CharField(max_length=200, verbose_name='函数名称'),
        ),
    ]
