from django.db import models

from competition.models import Competition
from team.models import Team


class LeagueTable(models.Model):
    competition = models.ForeignKey(Competition)
    league_caption = models.CharField(max_length=255)
    matchday = models.IntegerField()


class Standing(models.Model):
    league_table = models.ForeignKey(LeagueTable)
    team = models.ForeignKey(Team)
    position = models.PositiveIntegerField()
    played_games = models.PositiveIntegerField()
    points = models.PositiveIntegerField()
    goals = models.PositiveIntegerField()
    goals_against = models.PositiveIntegerField()
    goal_difference = models.IntegerField()
    wins = models.PositiveIntegerField()
    draws = models.PositiveIntegerField()
    losses = models.PositiveIntegerField()

    def has_position_changed(self, other_matchday_standing):
        """
        Checks position difference. Is normally used to compare matchday point differences.
        :param other_matchday_standing: The standing of a another matchday
        :return: True, if the position has changed; False otherwise.
        """
        if isinstance(other_matchday_standing, Standing):
            return self.position != other_matchday_standing.position
        raise ValueError(other_matchday_standing + ' is no valid Standing')

    def has_position_improved(self, other_matchday_standing):
        """
        Checks position improvement. Is normally used to compare matchday point improvements.
        :param other_matchday_standing: The standing of a another matchday
        :return: True, if the position has improved; False otherwise.
        """
        if isinstance(other_matchday_standing, Standing):
            return self.position < other_matchday_standing.position
        raise ValueError(other_matchday_standing + ' is no valid Standing')


class Home(models.Model):
    standing = models.ForeignKey(Standing)
    goals = models.PositiveIntegerField()
    goals_against = models.PositiveIntegerField()
    wins = models.PositiveIntegerField()
    draws = models.PositiveIntegerField()
    losses = models.PositiveIntegerField()


class Away(models.Model):
    standing = models.ForeignKey(Standing)
    goals = models.PositiveIntegerField()
    goals_against = models.PositiveIntegerField()
    wins = models.PositiveIntegerField()
    draws = models.PositiveIntegerField()
    losses = models.PositiveIntegerField()


class CupTable(models.Model):
    competition = models.ForeignKey(Competition)
    league_caption = models.CharField(max_length=255)
    matchday = models.IntegerField()


class Group(models.Model):
    cup_table = models.ForeignKey(CupTable)
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ['name']


class GroupStanding(models.Model):
    group = models.ForeignKey(Group)
    team = models.ForeignKey(Team)
    rank = models.PositiveSmallIntegerField()
    played_games = models.PositiveSmallIntegerField()
    crest_uri = models.URLField(null=True)
    points = models.PositiveSmallIntegerField()
    goals = models.PositiveSmallIntegerField()
    goals_against = models.PositiveSmallIntegerField()
    goal_difference = models.PositiveSmallIntegerField()

    def has_rank_changed(self, other_matchday_group_standing):
        """
        Checks position difference. Is normally used to compare matchday point differences.
        :param other_matchday_group_standing: The standing of a another matchday
        :return: True, if the position has changed; False otherwise.
        """
        if isinstance(other_matchday_group_standing, GroupStanding):
            return self.rank != other_matchday_group_standing.rank
        raise ValueError(other_matchday_group_standing + ' is no valid GroupStanding')

    def has_rank_improved(self, other_matchday_group_standing):
        """
        Checks position improvement. Is normally used to compare matchday point improvements.
        :param other_matchday_group_standing: The standing of a another matchday
        :return: True, if the position has improved; False otherwise.
        """
        if isinstance(other_matchday_group_standing, GroupStanding):
            return self.rank < other_matchday_group_standing.rank
        raise ValueError(other_matchday_group_standing + ' is no valid GroupStanding')
