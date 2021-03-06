# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-28 10:56
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('operations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserVote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vote_id', models.PositiveIntegerField(blank=True, null=True, verbose_name='数据ID')),
                ('vote_value', models.IntegerField(choices=[(1, '点赞'), (0, '🈚️无'), (-1, '点踩')], default=0, verbose_name='类型')),
                ('created', models.DateField(auto_now_add=True, verbose_name='收藏时间')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
                ('vote_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType', verbose_name='点赞对象')),
            ],
            options={
                'verbose_name': '用户点赞',
                'verbose_name_plural': '用户点赞',
            },
        ),
        migrations.RenameField(
            model_name='usermessage',
            old_name='add_time',
            new_name='created',
        ),
    ]
