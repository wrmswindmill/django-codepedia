# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-29 16:22
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0007_callgraph'),
    ]

    operations = [
        migrations.RenameField(
            model_name='callgraph',
            old_name='callee_function_id',
            new_name='callee_function',
        ),
        migrations.RenameField(
            model_name='callgraph',
            old_name='caller_function_id',
            new_name='caller_function',
        ),
    ]
