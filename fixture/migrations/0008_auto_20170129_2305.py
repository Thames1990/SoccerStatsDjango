# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-29 22:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fixture', '0007_auto_20170129_2301'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fixture',
            name='matchday',
            field=models.SmallIntegerField(),
        ),
    ]
