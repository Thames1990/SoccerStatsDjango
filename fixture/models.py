from django.db import models


class Fixture(models.Model):
    """
    The Fixture resource reflects a scheduled football game. A fixture typically belongs to a competition and is
    played on a certain matchday. Fixture appears as Main Resource and as Subresource of a Competition.
    """
    from competition.models import Competition
    from team.models import Team

    id = models.PositiveSmallIntegerField(primary_key=True)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_team')
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_team')
    date = models.DateTimeField(db_index=True)
    STATUS = (
        ('SCHEDULED', 'Geplant'),
        ('TIMED', 'Festgelegt'),
        ('POSTPONED', 'Verschoben'),
        ('IN_PLAY', 'Im Spiel'),
        ('CANCELED', 'Abgebrochen'),
        ('FINISHED', 'Beendet'),
        # TODO Ask author what FT should be
        ('FT', 'FT'),
    )
    status = models.CharField(db_index=True, max_length=255, choices=STATUS, null=True)
    matchday = models.PositiveSmallIntegerField()


class Result(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True)
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

# TODO Add Head2Head
