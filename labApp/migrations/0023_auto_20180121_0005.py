# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-01-20 21:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('labApp', '0022_auto_20180120_1806'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prodact',
            name='description',
            field=models.CharField(max_length=600, null=True, verbose_name='Описание'),
        ),
    ]
