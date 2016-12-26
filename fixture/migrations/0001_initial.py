# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-26 09:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('team', '__first__'),
        ('competition', '0001_initial'),
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
                ('date', models.DateTimeField(db_index=True)),
                ('status', models.CharField(choices=[('SCHEDULED', 'Geplant'), ('TIMED', 'Festgelegt'), ('POSTPONED', 'Verschoben'), ('IN_PLAY', 'Im Spiel'), ('CANCELED', 'Abgebrochen'), ('CANCELLED', 'Abgebrochen'), ('FINISHED', 'Beendet'), ('FT', 'FT')], db_index=True, max_length=255, null=True)),
                ('matchday', models.PositiveSmallIntegerField()),
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
            name='Odds',
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
                ('id', models.PositiveSmallIntegerField(primary_key=True, serialize=False)),
                ('goals_home_team', models.PositiveSmallIntegerField(null=True)),
                ('goals_away_team', models.PositiveSmallIntegerField(null=True)),
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
