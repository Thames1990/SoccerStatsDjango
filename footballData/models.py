import datetime
import inspect
from enum import Enum

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _


# TODO Implement '_links'
# TODO Figure out if NotImplemented raises a TypeError
# TODO Figure out if __ne__ is required
# TODO Are model __eq__ functions required? (https://github.com/django/django/blob/1.9.7/django/db/models/base.py#L477)

# TODO Remove when Django updates to 1.10 (enum serializiation)
class CompetitionTypeID(Enum):
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


class CupID(CompetitionTypeID):
    """
    IDs for cups
    """
    EC = 424
    """European Championships France 2016"""
    DFB = 432
    """DFB-Pokal 2016/17"""
    CL = 440
    """Champions League 2016/17"""


class LeagueID(CompetitionTypeID):
    """
    IDs for leagues
    """
    PL = 426
    """Premier League 2016/17"""
    ELC = 427
    """Championship 2016 / 17"""
    EL1 = 428
    """League One 2016 / 17"""
    BL1 = 430
    """1. Bundesliga 2016 / 17"""
    BL2 = 431
    """2. Bundesliga 2016 / 17"""
    DED = 433
    """Eredivisie 2016 / 17"""
    FL1 = 434
    """Ligue 1 2016 / 17"""
    FL2 = 435
    """Ligue 2 2016 / 17"""
    PD = 436
    """Primera Division 2016 / 17"""
    SD = 437
    """Liga Adelante 2016 / 17"""
    SA = 438
    """Serie A 2016 / 17"""
    PPL = 439
    """Primeira Liga 2016 / 17"""


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

    def __eq__(self, other):
        if isinstance(other, Competition):
            # TODO weaken equality
            return \
                self.id == other.id and \
                self.year == other.year and \
                self.current_matchday == other.current_matchday and \
                self.number_of_games == other.number_of_games and \
                self.last_updated == other.last_updated
        else:
            return NotImplemented


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

    # TODO Figure out default behaviour of non implemented __eq__ (each field equiality?)


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

    def __eq__(self, other):
        if isinstance(other, Team):
            return \
                self.name == other.name and \
                self.code == other.code and \
                self.short_name == other.short_name
        else:
            return NotImplemented


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

    def __eq__(self, other):
        if isinstance(other, Player):
            return \
                self.name == other.name and \
                self.date_of_birth == other.date_of_birth and \
                self.nationality == other.nationality
        else:
            return NotImplemented


# TODO If __eq__ are redundant: Create abstract Table model?
class LeagueTable(models.Model):
    league_caption = models.CharField(max_length=255)
    matchday = models.IntegerField()

    def __eq__(self, other):
        if isinstance(other, LeagueTable):
            # Check league for equality
            if not (self.league_caption == other.leagueCaption and self.matchday == other.matchday):
                return False
            other_standing_set = other.standing_set.all()
            # Check each team for equality
            for standing in self.standing_set.all():
                other_standing = other_standing_set.get(team_name=standing.team_name)
                if standing != other_standing:
                    return False
            return True
        else:
            return NotImplemented


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

    # TODO Refine equality
    def __eq__(self, other):
        if isinstance(other, Standing):
            return \
                isinstance(other, Standing) and \
                self.league_table == other.league_table and \
                self.position == other.position and \
                self.team_name == other.team_name and \
                self.played_games == other.played_games and \
                self.points == other.points
        else:
            return NotImplemented

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
            return self.position > other_matchday_standing.position
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

    def __eq__(self, other):
        if isinstance(other, CupTable):
            # Check league for equality
            if not (self.league_caption == other.leagueCaption and self.matchday == other.matchday):
                return False
            other_group_set = other.group_set.all()
            # Check each group for equality
            for group in self.group_set.all():
                other_group = other_group_set.get(name=group.name)
                if group != other_group:
                    return False

                # Check each team in the group for equality
                other_group_standing_set = other_group.groupstanding_set.all()
                for group_standing in group.groupstanding_set.all():
                    other_group_standing = other_group_standing_set.get(team=group_standing.team)
                    if group_standing != other_group_standing:
                        return False
            return True
        else:
            return NotImplemented


class Group(models.Model):
    cup_table = models.ForeignKey(CupTable)
    name = models.CharField(max_length=255)

    class Meta:
        # TODO Add ordering to other models
        ordering = ['name']

    # TODO Add and improve __str__ for all model, because debug and such
    def __str__(self):
        return self.cup_table.league_caption + ' ' + self.name


# TODO Merge Standing and GroupStanding
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

    # TODO Read model validation docs
    # def clean(self):
    #     if self.goal_difference != self.goals - self.goals_against:
    #         raise ValidationError(_('goal_difference has to be the subtraction of goals and goals_against'))

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
            return self.rank > other_matchday_group_standing.rank
        else:
            return NotImplemented
