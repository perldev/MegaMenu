# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-01-16 03:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_auto_20170114_1737'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chanel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, null=True, verbose_name='Title')),
            ],
        ),
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, null=True, verbose_name='Title')),
                ('content', models.TextField(blank=True, null=True, verbose_name='Title')),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date of adding')),
                ('ordering', models.IntegerField(default=0, verbose_name='ordering')),
                ('chanel', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='chanel', to='catalog.Chanel', verbose_name='Chanel')),
            ],
        ),
        migrations.CreateModel(
            name='Meta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(blank=True, max_length=255, null=True, verbose_name='Title')),
                ('keywords', models.CharField(blank=True, max_length=255, null=True, verbose_name='key words')),
                ('desc', models.CharField(blank=True, max_length=255, null=True, verbose_name='description')),
            ],
        ),
    ]
