# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-10-10 21:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qa', '0003_auto_20171010_2059'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='correct',
            field=models.BooleanField(default=True, verbose_name='正确与否'),
        ),
    ]
