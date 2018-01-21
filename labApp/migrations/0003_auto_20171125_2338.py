# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-25 20:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('labApp', '0002_auto_20171101_1623'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='customer_name',
        ),
        migrations.AlterField(
            model_name='order',
            name='prodact',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='labApp.Prodact', verbose_name='продукт'),
        ),
    ]
