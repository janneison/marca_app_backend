# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-29 12:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parametrizacion', '0003_auto_20171227_2103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='empresa',
            name='rut',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='persona',
            name='rut',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
