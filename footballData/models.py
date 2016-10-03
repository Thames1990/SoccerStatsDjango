from django.db import models


class Home(models.Model):
    goals = models.IntegerField()
    goalsAgainst = models.IntegerField()
    wins = models.IntegerField()
    draws = models.IntegerField()
    losses = models.IntegerField()


class Away(models.Model):
    goals = models.IntegerField()
    goalsAgainst = models.IntegerField()
    wins = models.IntegerField()
    draws = models.IntegerField()
    losses = models.IntegerField()


class Standing(models.Model):
    position = models.IntegerField()
    teamName = models.CharField(max_length=200)
    crestURI = models.CharField(max_length=200)
    playedGames = models.IntegerField()
    points = models.IntegerField()
    goals = models.IntegerField()
    goalsAgainst = models.IntegerField()
    goalDifference = models.IntegerField()
    wins = models.IntegerField()
    draws = models.IntegerField()
    losses = models.IntegerField()
    home = models.ForeignKey(Home)
    away = models.ForeignKey(Away)


class LeagueTable(models.Model):
    leagueCaption = models.CharField(max_length=200)
    matchday = models.IntegerField()
    standing = models.ForeignKey(Standing)

    def position_changed(self, last_matchday):
        if not isinstance(last_matchday, LeagueTable.standing.position):
            raise TypeError
        return self.standing.position != last_matchday

    def position_increased(self, last_matchday):
        if not isinstance(last_matchday, LeagueTable.standing.position):
            raise TypeError
        return self.standing.position > last_matchday

    def position_decreased(self, last_matchday):
        if not isinstance(last_matchday, LeagueTable.standing.position):
            raise TypeError
        return self.standing.position < last_matchday
