# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-26 22:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_auto_20170926_1654'),
    ]

    operations = [
        migrations.AddField(
            model_name='line',
            name='code',
            field=models.TextField(default='', verbose_name='代码'),
        ),
    ]
