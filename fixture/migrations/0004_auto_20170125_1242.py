# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-25 11:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fixture', '0003_auto_20170124_1657'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fixture',
            name='matchday',
            field=models.PositiveSmallIntegerField(),
        ),
    ]
