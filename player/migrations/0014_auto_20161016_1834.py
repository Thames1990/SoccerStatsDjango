# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-10-16 16:34
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0013_auto_20161016_1746'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='player',
            options={'ordering': ['position']},
        ),
    ]
