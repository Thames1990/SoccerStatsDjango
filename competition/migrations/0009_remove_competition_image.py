# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-27 17:44
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0008_auto_20170127_1825'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='competition',
            name='image',
        ),
    ]
