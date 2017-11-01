# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-11-01 16:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qa', '0016_auto_20171101_1646'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='question',
            index=models.Index(fields=['file_id', 'file_linenum', 'question_info'], name='qa_question_file_id_482a12_idx'),
        ),
        migrations.AddIndex(
            model_name='question',
            index=models.Index(fields=['function_id', 'file_linenum', 'question_info'], name='qa_question_functio_bca5e3_idx'),
        ),
        migrations.AddIndex(
            model_name='question',
            index=models.Index(fields=['function_id'], name='qa_question_functio_a54c36_idx'),
        ),
    ]
