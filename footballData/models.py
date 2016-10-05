from django.db import models


class LeagueTable(models.Model):
    league_caption = models.CharField(max_length=255)
    matchday = models.IntegerField()

    def __eq__(self, other):
        if isinstance(other, LeagueTable):
            return \
                isinstance(other, LeagueTable) and \
                self.league_caption == other.leagueCaption and \
                self.matchday == other.matchday
        else:
            return NotImplemented


class Standing(models.Model):
    league_table = models.ForeignKey(LeagueTable)
    position = models.IntegerField()
    team_name = models.CharField(max_length=255)
    crest_uri = models.URLField()
    played_games = models.IntegerField()
    points = models.IntegerField()
    goals = models.IntegerField()
    goals_against = models.IntegerField()
    goal_difference = models.IntegerField()
    wins = models.IntegerField()
    draws = models.IntegerField()
    losses = models.IntegerField()

    def __eq__(self, other):
        if isinstance(other, Standing):
            return \
                isinstance(other, Standing) and \
                self.league_table == other.league_table and \
                self.team_name == other.team_name and \
                self.played_games == other.played_games
        else:
            return NotImplemented


class Home(models.Model):
    standing = models.ForeignKey(Standing)
    goals = models.IntegerField()
    goals_against = models.IntegerField()
    wins = models.IntegerField()
    draws = models.IntegerField()
    losses = models.IntegerField()

    def __eq__(self, other):
        if isinstance(other, Home):
            return self.standing == other.standing
        else:
            return NotImplemented


class Away(models.Model):
    standing = models.ForeignKey(Standing)
    goals = models.IntegerField()
    goals_against = models.IntegerField()
    wins = models.IntegerField()
    draws = models.IntegerField()
    losses = models.IntegerField()

    def __eq__(self, other):
        if isinstance(other, Away):
            return self.standing == other.standing
        else:
            return NotImplemented
