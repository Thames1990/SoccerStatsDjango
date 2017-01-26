from django.db import models

from competition.models import Competition
from team.models import Team


class Table(models.Model):
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    matchday = models.PositiveSmallIntegerField()

    class Meta:
        get_latest_by = 'matchday'

    def __str__(self):
        return 'Table for %s on matchday %s' % (
            self.competition.caption,
            self.matchday,
        )


class Standing(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    position = models.PositiveSmallIntegerField()
    played_games = models.PositiveSmallIntegerField()
    points = models.PositiveSmallIntegerField()
    goals = models.PositiveSmallIntegerField()
    goals_against = models.PositiveSmallIntegerField()
    goal_difference = models.SmallIntegerField()
    wins = models.PositiveSmallIntegerField()
    draws = models.PositiveSmallIntegerField()
    d = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ['position']

    def __str__(self):
        return 'Standing for %s in %s at position %s on matchday %s' % (
            self.team.name,
            self.table.competition.caption,
            self.position,
            self.table.matchday,
        )

    def has_position_changed(self, previous_matchday_standing):
        """
        Checks position difference to the previous matchday.
        :param previous_matchday_standing: The standing of the previous matchday
        :return: True, if the position has changed; False otherwise.
        """
        return \
            self.position != previous_matchday_standing.position and \
            self.played_games > previous_matchday_standing.played_games

    def has_position_improved(self, previous_matchday_standing):
        """
        Checks position improvement from previous matchday.
        :param previous_matchday_standing: The standing of the previous matchday
        :return: True, if the position has improved; False otherwise.
        """
        return \
            self.position < previous_matchday_standing.position and \
            self.played_games > previous_matchday_standing.played_games


class HomeStanding(models.Model):
    standing = models.ForeignKey(Standing, on_delete=models.CASCADE)
    goals = models.PositiveSmallIntegerField()
    goals_against = models.PositiveSmallIntegerField()
    wins = models.PositiveSmallIntegerField()
    draws = models.PositiveSmallIntegerField()
    losses = models.PositiveSmallIntegerField()

    def __str__(self):
        return 'Home standing for %s in %s at position %s on matchday %s' % (
            self.standing.team.name,
            self.standing.table.competition.caption,
            self.standing.position,
            self.standing.table.matchday,
        )

    def goal_difference(self):
        return self.goals - self.goals_against


class AwayStanding(models.Model):
    standing = models.ForeignKey(Standing, on_delete=models.CASCADE)
    goals = models.PositiveSmallIntegerField()
    goals_against = models.PositiveSmallIntegerField()
    wins = models.PositiveSmallIntegerField()
    draws = models.PositiveSmallIntegerField()
    losses = models.PositiveSmallIntegerField()

    def __str__(self):
        return 'Away standing for %s in %s at position %s on matchday %s' % (
            self.standing.team.name,
            self.standing.table.competition.caption,
            self.standing.position,
            self.standing.table.matchday,
        )

    def goal_difference(self):
        return self.goals - self.goals_against


class Group(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return 'Group %s of %s' % (
            self.name,
            self.table.competition.caption
        )

    class Meta:
        ordering = ['name']


class GroupStanding(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    rank = models.PositiveSmallIntegerField()
    played_games = models.PositiveSmallIntegerField()
    crest_uri = models.URLField(null=True)
    points = models.PositiveSmallIntegerField()
    goals = models.PositiveSmallIntegerField()
    goals_against = models.PositiveSmallIntegerField()
    goal_difference = models.SmallIntegerField()

    class Meta:
        ordering = ['rank']

    def __str__(self):
        return 'Group standing for %s in %s at rank %s on matchday %s' % (
            self.team.name,
            self.table.competition.caption,
            self.rank,
            self.table.matchday,
        )

    def has_rank_changed(self, previous_matchday_group_standing):
        """
        Checks rank difference to the previous matchday.
        :param previous_matchday_group_standing: The group standing of the previous matchday
        :return: True, if the rank has changed; False otherwise.
        """
        return \
            self.rank != previous_matchday_group_standing.rank and \
            self.played_games > previous_matchday_group_standing.played_games

    def has_rank_improved(self, previous_matchday_group_standing):
        """
        Checks rank improvement from previous matchday.
        :param previous_matchday_group_standing: The group standing of the previous matchday
        :return: True, if the rank has improved; False otherwise.
        """
        return \
            self.rank < previous_matchday_group_standing.rank and \
            self.played_games > previous_matchday_group_standing.played_games
