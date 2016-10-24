from django.db import models


class Fixture(models.Model):
    from competition.models import Competition
    from team.models import Team

    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_team')
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_team')
    date = models.DateTimeField(db_index=True)
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
    status = models.CharField(db_index=True, max_length=255, choices=STATUS)
    matchday = models.PositiveSmallIntegerField()


class Result(models.Model):
    fixture = models.ForeignKey(Fixture, on_delete=models.CASCADE)
    goals_home_team = models.PositiveSmallIntegerField(null=True)
    goals_away_team = models.PositiveSmallIntegerField(null=True)


class HalfTime(models.Model):
    result = models.ForeignKey(Result, on_delete=models.CASCADE)
    goals_home_team = models.PositiveSmallIntegerField()
    goals_away_team = models.PositiveSmallIntegerField()


class ExtraTime(models.Model):
    result = models.ForeignKey(Result, on_delete=models.CASCADE)
    goals_home_team = models.PositiveSmallIntegerField()
    goals_away_team = models.PositiveSmallIntegerField()


class PenaltyShootout(models.Model):
    result = models.ForeignKey(Result, on_delete=models.CASCADE)
    goals_home_team = models.PositiveSmallIntegerField()
    goals_away_team = models.PositiveSmallIntegerField()


class Odds(models.Model):
    fixture = models.ForeignKey(Fixture, on_delete=models.CASCADE)
    home_win = models.FloatField()
    draw = models.FloatField()
    away_win = models.FloatField()
