# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-12 00:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asistencia', '0007_auto_20180216_1032'),
    ]

    operations = [
        migrations.AddField(
            model_name='horario',
            name='cantidadHoras',
            field=models.IntegerField(default=24),
        ),
        migrations.AddField(
            model_name='horario',
            name='jornada',
            field=models.IntegerField(choices=[(1, 'Lunes'), (2, 'Martes'), (3, 'Miercoles'), (4, 'Jueves'), (5, 'Viernes'), (6, 'Sabado'), (7, 'Domingo')], default=1),
        ),
        migrations.AlterField(
            model_name='horario',
            name='primerDia',
            field=models.IntegerField(choices=[(1, 'Lunes'), (2, 'Martes'), (3, 'Miercoles'), (4, 'Jueves'), (5, 'Viernes'), (6, 'Sabado'), (7, 'Domingo')], default=1),
        ),
        migrations.AlterField(
            model_name='horario',
            name='ultimoDia',
            field=models.IntegerField(choices=[(1, 'Lunes'), (2, 'Martes'), (3, 'Miercoles'), (4, 'Jueves'), (5, 'Viernes'), (6, 'Sabado'), (7, 'Domingo')], default=6),
        ),
    ]