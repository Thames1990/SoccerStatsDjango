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
    status = models.CharField(max_length=255, null=True)
    matchday = models.PositiveSmallIntegerField()

    def __str__(self):
        return 'id: %s | %s | %s vs. %s | %s | %s, matchday: %s' % (
            self.id,
            self.competition.league,
            self.home_team.name,
            self.away_team.name,
            self.date,
            self.status,
            self.matchday,
        )


# TODO Think about moving models below into Fixture
class Result(models.Model):
    fixture = models.ForeignKey(Fixture, on_delete=models.CASCADE)
    goals_home_team = models.PositiveSmallIntegerField()
    goals_away_team = models.PositiveSmallIntegerField()

    def __str__(self):
        return 'id: %s | fixture id: %s | %s:%s' % (
            self.id,
            self.fixture_id,
            self.goals_home_team,
            self.goals_away_team,
        )


class HalfTime(models.Model):
    result = models.ForeignKey(Result, on_delete=models.CASCADE)
    goals_home_team = models.PositiveSmallIntegerField()
    goals_away_team = models.PositiveSmallIntegerField()

    def __str__(self):
        return 'id: %s | result id: %s | %s:%s' % (
            self.id,
            self.result_id,
            self.goals_home_team,
            self.goals_away_team,
        )


class ExtraTime(models.Model):
    result = models.ForeignKey(Result, on_delete=models.CASCADE)
    goals_home_team = models.PositiveSmallIntegerField()
    goals_away_team = models.PositiveSmallIntegerField()

    def __str__(self):
        return 'id: %s | result id: %s | %s:%s' % (
            self.id,
            self.result_id,
            self.goals_home_team,
            self.goals_away_team,
        )


class PenaltyShootout(models.Model):
    result = models.ForeignKey(Result, on_delete=models.CASCADE)
    goals_home_team = models.PositiveSmallIntegerField()
    goals_away_team = models.PositiveSmallIntegerField()

    def __str__(self):
        return 'id: %s | result id: %s | %s:%s' % (
            self.id,
            self.result_id,
            self.goals_home_team,
            self.goals_away_team,
        )


class Odd(models.Model):
    fixture = models.ForeignKey(Fixture, on_delete=models.CASCADE)
    home_win = models.FloatField()
    draw = models.FloatField()
    away_win = models.FloatField()

    def __str__(self):
        return 'id: %s | fixture id: %s | home win: %s | draw: %s | away win: %s' % (
            self.id,
            self.fixture_id,
            self.home_win,
            self.draw,
            self.away_win,
        )

# TODO Add Head2Head
