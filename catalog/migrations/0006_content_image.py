# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-01-16 06:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0005_chanel_ext_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='content',
            name='image',
            field=models.ImageField(blank=True, max_length=254, null=True, upload_to='img'),
        ),
    ]
