# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-01-21 22:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0008_auto_20170121_2019'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='full_desc',
            field=models.TextField(blank=True, max_length=255, null=True, verbose_name='\u043f\u043e\u043b\u043d\u043e\u0435 \u043e\u043f\u0438\u0441\u0430\u043d\u0438\u0435'),
        ),
    ]
