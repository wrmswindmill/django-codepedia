# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-25 22:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
    ]

    operations = [
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='编程语言')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '编程语言',
                'verbose_name_plural': '编程语言',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='工程名称')),
                ('path', models.CharField(max_length=200, verbose_name='工程全路径')),
                ('rel_path', models.CharField(max_length=200, verbose_name='工程相对路径')),
                ('github', models.URLField(max_length=100, verbose_name='Github网址')),
                ('ossean', models.URLField(max_length=100, verbose_name='Ossean网址')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.Language', verbose_name='编程语言')),
                ('tags', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
            options={
                'verbose_name': '工程',
                'verbose_name_plural': '工程',
            },
        ),
    ]
