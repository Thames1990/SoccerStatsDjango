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
    date = models.DateTimeField()
    STATUS = (
        ('SCHEDULED', 'Geplant'),
        ('TIMED', 'Festgelegt'),
        ('POSTPONED', 'Verschoben'),
        ('IN_PLAY', 'Im Spiel'),
        ('CANCELED', 'Abgebrochen'),
        ('CANCELLED', 'Abgebrochen'),
        ('FINISHED', 'Beendet'),
        # TODO Ask author what FT should be
        ('FT', 'FT'),
    )
    status = models.CharField(max_length=255, choices=STATUS, null=True)
    matchday = models.IntegerField()

    def __str__(self):
        return '%s vs. %s playing in %s on %s (%s) is %s' % (
            self.home_team.name,
            self.away_team.name,
            self.competition.caption,
            self.date,
            self.matchday,
            self.status,
        )


class Result(models.Model):
    fixture = models.ForeignKey(Fixture, on_delete=models.CASCADE)
    goals_home_team = models.PositiveSmallIntegerField()
    goals_away_team = models.PositiveSmallIntegerField()

    def __str__(self):
        return '%s | result: %s:%s' % (
            self.fixture,
            self.goals_home_team,
            self.goals_away_team,
        )


class HalfTime(models.Model):
    result = models.ForeignKey(Result, on_delete=models.CASCADE)
    goals_home_team = models.PositiveSmallIntegerField()
    goals_away_team = models.PositiveSmallIntegerField()

    def __str__(self):
        return '%s | half time result: %s:%s' % (
            self.result,
            self.goals_home_team,
            self.goals_away_team,
        )


class ExtraTime(models.Model):
    result = models.ForeignKey(Result, on_delete=models.CASCADE)
    goals_home_team = models.PositiveSmallIntegerField()
    goals_away_team = models.PositiveSmallIntegerField()

    def __str__(self):
        return '%s | extra time result: %s:%s' % (
            self.result,
            self.goals_home_team,
            self.goals_away_team,
        )


class PenaltyShootout(models.Model):
    result = models.ForeignKey(Result, on_delete=models.CASCADE)
    goals_home_team = models.PositiveSmallIntegerField()
    goals_away_team = models.PositiveSmallIntegerField()

    def __str__(self):
        return '%s | penalty shootout result: %s:%s' % (
            self.result,
            self.goals_home_team,
            self.goals_away_team,
        )


class Odd(models.Model):
    fixture = models.ForeignKey(Fixture, on_delete=models.CASCADE)
    home_win = models.FloatField()
    draw = models.FloatField()
    away_win = models.FloatField()

    def __str__(self):
        return '%s | home win: %s | draw: %s | away win: %s' % (
            self.fixture,
            self.home_win,
            self.draw,
            self.away_win,
        )

# TODO Add Head2Head
