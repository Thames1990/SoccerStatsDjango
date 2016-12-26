from django.db import models

from competition.models import Competition
from team.models import Team


class Table(models.Model):
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    league_caption = models.CharField(max_length=255)
    matchday = models.IntegerField()

    class Meta:
        get_latest_by = 'matchday'


class Standing(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    position = models.PositiveIntegerField()
    played_games = models.PositiveIntegerField()
    points = models.PositiveIntegerField()
    goals = models.PositiveIntegerField()
    goals_against = models.PositiveIntegerField()
    goal_difference = models.IntegerField()
    wins = models.PositiveIntegerField()
    draws = models.PositiveIntegerField()
    losses = models.PositiveIntegerField()

    class Meta:
        ordering = ['position']

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


class HomeStanding(models.Model):
    standing = models.ForeignKey(Standing, on_delete=models.CASCADE)
    goals = models.PositiveIntegerField()
    goals_against = models.PositiveIntegerField()
    wins = models.PositiveIntegerField()
    draws = models.PositiveIntegerField()
    losses = models.PositiveIntegerField()

    def goal_difference(self):
        return self.goals - self.goals_against


class AwayStanding(models.Model):
    standing = models.ForeignKey(Standing, on_delete=models.CASCADE)
    goals = models.PositiveIntegerField()
    goals_against = models.PositiveIntegerField()
    wins = models.PositiveIntegerField()
    draws = models.PositiveIntegerField()
    losses = models.PositiveIntegerField()

    def goal_difference(self):
        return self.goals - self.goals_against


class Group(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)


class GroupStanding(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    rank = models.PositiveSmallIntegerField()
    played_games = models.PositiveSmallIntegerField()
    crest_uri = models.URLField(null=True)
    points = models.PositiveSmallIntegerField()
    goals = models.PositiveSmallIntegerField()
    goals_against = models.PositiveSmallIntegerField()
    goal_difference = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ['rank']

    def has_rank_changed(self, other_matchday_group_standing):
        """
        Checks rank difference. Is normally used to compare matchday point differences.
        :param other_matchday_group_standing: The group standing of a another matchday
        :return: True, if the rank has changed; False otherwise.
        """
        if isinstance(other_matchday_group_standing, GroupStanding):
            return self.rank != other_matchday_group_standing.rank
        raise ValueError(other_matchday_group_standing + ' is no valid GroupStanding')

    def has_rank_improved(self, other_matchday_group_standing):
        """
        Checks rank improvement. Is normally used to compare matchday point improvements.
        :param other_matchday_group_standing: The group standing of a another matchday
        :return: True, if the rank has improved; False otherwise.
        """
        if isinstance(other_matchday_group_standing, GroupStanding):
            return self.rank < other_matchday_group_standing.rank
        raise ValueError(other_matchday_group_standing + ' is no valid GroupStanding')
