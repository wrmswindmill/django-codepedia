# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-10-13 19:43
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('qa', '0009_auto_20171013_1044'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(default='', verbose_name='内容')),
                ('created', models.DateField(auto_now_add=True, verbose_name='评论时间')),
            ],
            options={
                'verbose_name': '问题评论',
                'verbose_name_plural': '问题评论',
            },
        ),
        migrations.AlterModelOptions(
            name='question',
            options={'ordering': ['file_linenum', 'question_info'], 'verbose_name': '问题', 'verbose_name_plural': '问题'},
        ),
        migrations.AlterField(
            model_name='question',
            name='file_id',
            field=models.IntegerField(null=True, verbose_name='文件'),
        ),
        migrations.AlterField(
            model_name='question',
            name='function_linenum',
            field=models.IntegerField(null=True, verbose_name='方法行号'),
        ),
        migrations.AddField(
            model_name='questioncomment',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question_comment', to='qa.Question', verbose_name='问题'),
        ),
        migrations.AddField(
            model_name='questioncomment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户'),
        ),
    ]