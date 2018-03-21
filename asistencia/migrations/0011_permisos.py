# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-20 01:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('parametrizacion', '0010_auto_20180301_1310'),
        ('asistencia', '0010_auto_20180316_1358'),
    ]

    operations = [
        migrations.CreateModel(
            name='Permisos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('modified_on', models.DateTimeField(auto_now=True)),
                ('fechaInicio', models.DateField()),
                ('fechaFin', models.DateField()),
                ('tipoAsignacion', models.IntegerField(choices=[(1, 'Vacaciones'), (2, 'Licencia Medica'), (3, 'Permiso Especial'), (4, 'Entrada con Retraso'), (5, 'Salida Anticipada')], default=1)),
                ('observacion', models.CharField(max_length=255)),
                ('autorizado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parametrizacion.Persona')),
                ('estado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parametrizacion.Estado')),
            ],
            options={
                'permissions': (('can_see_all', 'Ver todos'), ('can_see_owner', 'Solo los que creo')),
                'abstract': False,
            },
        ),
    ]