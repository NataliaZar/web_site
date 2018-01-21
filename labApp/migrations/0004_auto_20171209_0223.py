# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-08 23:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('labApp', '0003_auto_20171125_2338'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProdactCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=30, verbose_name='Категория товара')),
            ],
        ),
        migrations.RemoveField(
            model_name='customer',
            name='email',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='user',
        ),
        migrations.AddField(
            model_name='customer',
            name='images',
            field=models.ImageField(blank=True, default='user/user_icon.png', upload_to='user/', verbose_name='Фотография'),
        ),
        migrations.AddField(
            model_name='prodact',
            name='images',
            field=models.ImageField(blank=True, default='prodact/prodact_icon.png', upload_to='prodact/', verbose_name='Фотография'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='birthday',
            field=models.DateField(verbose_name='День рождения'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='first_name',
            field=models.CharField(max_length=30, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='last_name',
            field=models.CharField(max_length=30, verbose_name='Фамилия'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='sex',
            field=models.CharField(max_length=1, verbose_name='Пол'),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Дата заказа'),
        ),
        migrations.AlterField(
            model_name='order',
            name='prodact',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='labApp.Prodact', verbose_name='Продукт'),
        ),
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='labApp.Customer', verbose_name='Покупатель'),
        ),
        migrations.AlterField(
            model_name='prodact',
            name='description',
            field=models.CharField(max_length=255, null=True, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='prodact',
            name='price',
            field=models.FloatField(max_length=10, verbose_name='Цена'),
        ),
        migrations.AlterField(
            model_name='prodact',
            name='prodact_name',
            field=models.CharField(max_length=30, verbose_name='Наименование товара'),
        ),
        migrations.AddField(
            model_name='prodact',
            name='category',
            field=models.ManyToManyField(blank=True, to='labApp.ProdactCategory', verbose_name='Категория товара'),
        ),
    ]
