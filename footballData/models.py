import datetime
import inspect
from enum import Enum

from django.db import models


# TODO Add references to Cometition
# TODO Remove when Django updates to 1.10 (enum serializiation)
class CompetitionID(Enum):
    """
    Abstract enum for competition types (cup or league)
    """

    @classmethod
    def choices(cls):
        """
        Creates the tuple structure for Django model choices
        :return: Tuple of enum choices
        """
        # get all members of the class
        members = inspect.getmembers(cls, lambda m: not (inspect.isroutine(m)))
        # filter down to just properties
        props = [m for m in members if not (m[0][:2] == '__')]
        # format into django choice tuple
        choices = tuple([(str(p[1].value), p[0]) for p in props])
        return choices


class CupID(CompetitionID):
    """
    IDs for cups
    """
    EC = 424
    """European Championships France 2016"""
    # DFB = 432
    """
    DFB-Pokal 2016/17
    Currently not available.
    """
    CL = 440
    """Champions League 2016/17"""


class LeagueID(CompetitionID):
    """
    IDs for leagues
    """
    PL = 426
    """Premier League 2016/17"""
    ELC = 427
    """Championship 2016/17"""
    EL1 = 428
    """League One 2016/17"""
    BL1 = 430
    """1. Bundesliga 2016/17"""
    BL2 = 431
    """2. Bundesliga 2016/17"""
    DED = 433
    """Eredivisie 2016/17"""
    FL1 = 434
    """Ligue 1 2016/17"""
    FL2 = 435
    """Ligue 2 2016/17"""
    PD = 436
    """Primera Division 2016/17"""
    SD = 437
    """Liga Adelante 2016/17"""
    SA = 438
    """Serie A 2016/17"""
    PPL = 439
    """Primeira Liga 2016/17"""


class Competition(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True)
    caption = models.CharField(max_length=255)
    league = models.CharField(max_length=255, choices=LeagueID.choices())
    YEARS = [(r, r) for r in range(1980, (datetime.datetime.now().year + 1))]
    year = models.IntegerField(choices=YEARS)
    current_matchday = models.PositiveSmallIntegerField()
    number_of_matchdays = models.PositiveSmallIntegerField()
    number_of_teams = models.PositiveSmallIntegerField()
    number_of_games = models.PositiveSmallIntegerField()
    last_updated = models.DateTimeField()


class Fixture(models.Model):
    date = models.DateTimeField()
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
    status = models.CharField(max_length=255, choices=STATUS)
    matchday = models.PositiveSmallIntegerField()
    home_team_name = models.CharField(max_length=255)
    away_team_name = models.CharField(max_length=255)


class Result(models.Model):
    fixture = models.ForeignKey(Fixture)
    goals_home_team = models.PositiveSmallIntegerField()
    goals_away_team = models.PositiveSmallIntegerField()


# TODO DRY
class HalfTime(models.Model):
    result = models.ForeignKey(Result)
    goals_home_team = models.PositiveSmallIntegerField()
    goals_away_team = models.PositiveSmallIntegerField()


class ExtraTime(models.Model):
    result = models.ForeignKey(Result)
    goals_home_team = models.PositiveSmallIntegerField()
    goals_away_team = models.PositiveSmallIntegerField()


class PenaltyShooutout(models.Model):
    result = models.ForeignKey(Result)
    goals_home_team = models.PositiveSmallIntegerField()
    goals_away_team = models.PositiveSmallIntegerField()


class Odds(models.Model):
    fixture = models.ForeignKey(Fixture)
    home_win = models.DecimalField(max_digits=2, decimal_places=2)
    draw = models.DecimalField(max_digits=2, decimal_places=2)
    away_win = models.DecimalField(max_digits=2, decimal_places=2)


class Team(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    short_name = models.CharField(max_length=255)
    squad_market_value = models.PositiveIntegerField
    crest_url = models.URLField(null=True)


class Player(models.Model):
    name = models.CharField(max_length=255)
    KEEPER = 1
    RIGHT_BACK = 2
    CENTRE_BACK = 4
    LEFT_BACK = 3
    DEFENSIVE_MIDFIELD = 6
    CENTRAL_MIDFIELD = 8
    ATTACKING_MIDFIELD = 10
    RIGHT_WING = 7
    CENTRE_FORWARD = 9
    LEFT_WING = 11
    POSITION = (
        (KEEPER, 'Keeper'),
        (RIGHT_BACK, 'Right-Back'),
        (CENTRE_BACK, 'Centre Back'),
        (LEFT_BACK, 'Left-Back'),
        (DEFENSIVE_MIDFIELD, 'Defensive Midfield'),
        (CENTRAL_MIDFIELD, 'Central Midfield'),
        (ATTACKING_MIDFIELD, 'Attacking Midfield'),
        (RIGHT_WING, 'Right Wing'),
        (CENTRE_FORWARD, 'Centre Forward'),
        (LEFT_WING, 'Left Wing'),
    )
    position = models.CharField(max_length=255, choices=POSITION)
    jersey_number = models.PositiveSmallIntegerField
    date_of_birth = models.DateField()
    nationality = models.CharField(max_length=255)
    contract_until = models.DateField()
    market_value = models.PositiveIntegerField()


class LeagueTable(models.Model):
    league_caption = models.CharField(max_length=255)
    matchday = models.IntegerField()


class Standing(models.Model):
    league_table = models.ForeignKey(LeagueTable)
    position = models.PositiveIntegerField()
    team_name = models.CharField(max_length=255)
    crest_uri = models.URLField(null=True)
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
        else:
            return NotImplemented

    def has_position_improved(self, other_matchday_standing):
        """
        Checks position improvement. Is normally used to compare matchday point improvements.
        :param other_matchday_standing: The standing of a another matchday
        :return: True, if the position has improved; False otherwise.
        """
        if isinstance(other_matchday_standing, Standing):
            return self.position < other_matchday_standing.position
        else:
            return NotImplemented


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
    league_caption = models.CharField(max_length=255)
    matchday = models.IntegerField()


class Group(models.Model):
    cup_table = models.ForeignKey(CupTable)
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ['name']


class GroupStanding(models.Model):
    group = models.ForeignKey(Group)
    rank = models.PositiveSmallIntegerField()
    team = models.CharField(max_length=255)
    team_id = models.PositiveSmallIntegerField()
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
        else:
            return NotImplemented

    def has_rank_improved(self, other_matchday_group_standing):
        """
        Checks position improvement. Is normally used to compare matchday point improvements.
        :param other_matchday_group_standing: The standing of a another matchday
        :return: True, if the position has improved; False otherwise.
        """
        if isinstance(other_matchday_group_standing, GroupStanding):
            return self.rank < other_matchday_group_standing.rank
        else:
            return NotImplemented
