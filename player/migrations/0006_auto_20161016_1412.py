# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-10-16 14:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0005_auto_20161016_1410'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='market_value',
            field=models.PositiveIntegerField(null=True),
        ),
    ]