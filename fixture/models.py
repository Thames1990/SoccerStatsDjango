from django.db import models


class Fixture(models.Model):
    date = models.DateTimeField()
    SCHEDULED = 1
    TIMED = 2
    POSTPONED = 3
    IN_PLAY = 4
    CANCELED = 5
    FINISHED = 6
    STATUS = (
        (SCHEDULED, 'SCHEDULED'),
        (TIMED, 'TIMED'),
        (POSTPONED, 'POSTPONED'),
        (IN_PLAY, 'IN_PLAY'),
        (CANCELED, 'CANCELED'),
        (FINISHED, 'FINISHED'),
    )
    status = models.CharField(max_length=255, choices=STATUS)
    matchday = models.PositiveSmallIntegerField()
    home_team_name = models.CharField(max_length=255)
    away_team_name = models.CharField(max_length=255)


class Result(models.Model):
    fixture = models.ForeignKey(Fixture)
    goals_home_team = models.PositiveSmallIntegerField()
    goals_away_team = models.PositiveSmallIntegerField()


class HalfTime(models.Model):
    result = models.ForeignKey(Result)
    goals_home_team = models.PositiveSmallIntegerField()
    goals_away_team = models.PositiveSmallIntegerField()


class ExtraTime(models.Model):
    result = models.ForeignKey(Result)
    goals_home_team = models.PositiveSmallIntegerField()
    goals_away_team = models.PositiveSmallIntegerField()


class PenaltyShooutout(models.Model):
    result = models.ForeignKey(Result)
    goals_home_team = models.PositiveSmallIntegerField()
    goals_away_team = models.PositiveSmallIntegerField()


class Odds(models.Model):
    fixture = models.ForeignKey(Fixture)
    home_win = models.DecimalField(max_digits=2, decimal_places=2)
    draw = models.DecimalField(max_digits=2, decimal_places=2)
    away_win = models.DecimalField(max_digits=2, decimal_places=2)
