# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-11-12 22:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_grade_school'),
    ]

    operations = [
        migrations.AddField(
            model_name='grade',
            name='college',
            field=models.CharField(default='', max_length=50, verbose_name='学院'),
        ),
    ]
