# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-26 12:23
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0003_competition_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='competition',
            name='image',
        ),
    ]
