from django.db import models

from competition.models import Competition
from team.models import Team


# TODO merge tables since they're equivalent?
class LeagueTable(models.Model):
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    matchday = models.IntegerField()

    class Meta:
        unique_together = ('competition', 'matchday')


class Standing(models.Model):
    league_table = models.ForeignKey(LeagueTable, on_delete=models.CASCADE)
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
        unique_together = ('league_table', 'team', 'played_games')

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
    standing = models.ForeignKey(Standing, on_delete=models.CASCADE)
    goals = models.PositiveIntegerField()
    goals_against = models.PositiveIntegerField()
    wins = models.PositiveIntegerField()
    draws = models.PositiveIntegerField()
    losses = models.PositiveIntegerField()


class Away(models.Model):
    standing = models.ForeignKey(Standing, on_delete=models.CASCADE)
    goals = models.PositiveIntegerField()
    goals_against = models.PositiveIntegerField()
    wins = models.PositiveIntegerField()
    draws = models.PositiveIntegerField()
    losses = models.PositiveIntegerField()


class CupTable(models.Model):
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    matchday = models.IntegerField()

    class Meta:
        unique_together = ('competition', 'matchday')


class Group(models.Model):
    cup_table = models.ForeignKey(CupTable, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ['name']
        unique_together = ('cup_table', 'name')


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
