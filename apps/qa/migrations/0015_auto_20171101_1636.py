# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-11-01 16:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qa', '0014_auto_20171101_1629'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='file_id',
            field=models.IntegerField(null=True, verbose_name='文件'),
        ),
        migrations.AddIndex(
            model_name='question',
            index=models.Index(fields=['file_id', 'file_linenum'], name='qa_question_file_id_205ed1_idx'),
        ),
        migrations.AddIndex(
            model_name='question',
            index=models.Index(fields=['file_id'], name='qa_question_file_id_901087_idx'),
        ),
    ]
