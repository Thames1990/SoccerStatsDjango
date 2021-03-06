# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-29 22:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('competition', '0001_initial'),
        ('team', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExtraTime',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goals_home_team', models.PositiveSmallIntegerField()),
                ('goals_away_team', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Fixture',
            fields=[
                ('id', models.PositiveSmallIntegerField(primary_key=True, serialize=False)),
                ('date', models.DateTimeField()),
                ('status', models.CharField(choices=[('SCHEDULED', 'Geplant'), ('TIMED', 'Festgelegt'), ('POSTPONED', 'Verschoben'), ('IN_PLAY', 'Im Spiel'), ('CANCELED', 'Abgebrochen'), ('CANCELLED', 'Abgebrochen'), ('FINISHED', 'Beendet'), ('FT', 'FT')], max_length=255, null=True)),
                ('matchday', models.SmallIntegerField()),
                ('away_team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='away_team', to='team.Team')),
                ('competition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='competition.Competition')),
                ('home_team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='home_team', to='team.Team')),
            ],
        ),
        migrations.CreateModel(
            name='HalfTime',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goals_home_team', models.PositiveSmallIntegerField()),
                ('goals_away_team', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Odd',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('home_win', models.FloatField()),
                ('draw', models.FloatField()),
                ('away_win', models.FloatField()),
                ('fixture', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fixture.Fixture')),
            ],
        ),
        migrations.CreateModel(
            name='PenaltyShootout',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goals_home_team', models.PositiveSmallIntegerField()),
                ('goals_away_team', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goals_home_team', models.PositiveSmallIntegerField()),
                ('goals_away_team', models.PositiveSmallIntegerField()),
                ('fixture', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fixture.Fixture')),
            ],
        ),
        migrations.AddField(
            model_name='penaltyshootout',
            name='result',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fixture.Result'),
        ),
        migrations.AddField(
            model_name='halftime',
            name='result',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fixture.Result'),
        ),
        migrations.AddField(
            model_name='extratime',
            name='result',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fixture.Result'),
        ),
    ]
