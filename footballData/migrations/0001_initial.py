# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-10-02 19:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Away',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goals', models.IntegerField()),
                ('goalsAgainst', models.IntegerField()),
                ('wins', models.IntegerField()),
                ('draws', models.IntegerField()),
                ('losses', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Home',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goals', models.IntegerField()),
                ('goalsAgainst', models.IntegerField()),
                ('wins', models.IntegerField()),
                ('draws', models.IntegerField()),
                ('losses', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='LeagueTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('leagueCaption', models.CharField(max_length=200)),
                ('matchday', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Standing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.IntegerField()),
                ('teamName', models.CharField(max_length=200)),
                ('crestURI', models.CharField(max_length=200)),
                ('playedGames', models.IntegerField()),
                ('points', models.IntegerField()),
                ('goals', models.IntegerField()),
                ('goalsAgainst', models.IntegerField()),
                ('goalDifference', models.IntegerField()),
                ('wins', models.IntegerField()),
                ('draws', models.IntegerField()),
                ('losses', models.IntegerField()),
                ('away', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='footballData.Away')),
                ('home', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='footballData.Home')),
            ],
        ),
        migrations.AddField(
            model_name='leaguetable',
            name='standing',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='footballData.Standing'),
        ),
    ]
