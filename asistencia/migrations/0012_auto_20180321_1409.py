# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-21 14:09
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asistencia', '0011_permisos'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Permisos',
            new_name='Permiso',
        ),
    ]