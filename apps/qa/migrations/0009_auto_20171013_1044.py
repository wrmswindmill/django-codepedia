# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-10-13 10:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qa', '0008_auto_20171012_0935'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='question_info',
            field=models.CharField(choices=[('1', '错误程度'), ('2', '错误行号'), ('3', '错误类型')], max_length=3, null=True, verbose_name='问题信息'),
        ),
        migrations.AlterField(
            model_name='question',
            name='question_level',
            field=models.CharField(choices=[('jd', '简单'), ('zd', '中等'), ('n', '难')], default='jd', max_length=5, verbose_name='问题级别'),
        ),
        migrations.AlterField(
            model_name='question',
            name='question_source',
            field=models.CharField(choices=[('1', '系统'), ('2', '用户')], default='1', max_length=3, verbose_name='问题来源'),
        ),
    ]