# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-02-02 10:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0015_auto_20170127_1005'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='group',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='\u0413\u0440\u0443\u043f\u043f\u0430 \u043f\u0430\u043a\u0435\u0442\u0430'),
        ),
    ]
