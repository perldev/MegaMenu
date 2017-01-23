# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-01-21 20:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0007_product_pub_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='brand',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.Brand', verbose_name='\u0411\u0440\u0435\u043d\u0434'),
        ),
        migrations.AddField(
            model_name='product',
            name='status',
            field=models.BooleanField(default=True, verbose_name='\u0410\u043a\u0442\u0438\u0432\u043d\u044b\u0439'),
        ),
    ]