import datetime
from enum import Enum
import inspect

from django.db import models


# TODO Remove when Django updates to 1.10 (enum serializiation)
class CompetitionID(Enum):
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
    # TODO Combine choices for CupID and LeagueID
    league = models.CharField(max_length=255, choices=LeagueID.choices())
    YEARS = [(r, r) for r in range(1980, (datetime.datetime.now().year + 1))]
    year = models.IntegerField(choices=YEARS)
    current_matchday = models.PositiveSmallIntegerField()
    number_of_matchdays = models.PositiveSmallIntegerField()
    number_of_teams = models.PositiveSmallIntegerField()
    number_of_games = models.PositiveSmallIntegerField()
    last_updated = models.DateTimeField()
