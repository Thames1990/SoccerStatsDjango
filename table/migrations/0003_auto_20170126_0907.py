# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-26 08:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('table', '0002_auto_20170125_2137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupstanding',
            name='goal_difference',
            field=models.SmallIntegerField(),
        ),
        migrations.AlterField(
            model_name='standing',
            name='goal_difference',
            field=models.SmallIntegerField(),
        ),
    ]
