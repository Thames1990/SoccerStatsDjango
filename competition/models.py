import datetime
from enum import Enum

from django.db import models


class CompetitionId(Enum):
    @classmethod
    def choices(cls):
        """
        Creates the tuple structure for Django model choices
        :return: Tuple of enum choices
        """
        import inspect
        members = inspect.getmembers(cls, lambda m: not (inspect.isroutine(m)))
        props = [m for m in members if not (m[0][:2] == '__')]
        choices = tuple([(str(p[1].value), p[0]) for p in props])
        return choices

    @classmethod
    def reverse_lookup(cls, value):
        """
        Allows enum reverse lookup (value -> key)
        :param value: Value, whose key is searched
        :return: Key matching value
        """
        for subclass in cls.__subclasses__():
            for _, member in subclass.__members__.items():
                if member.name == value:
                    return member


class CupId(CompetitionId):
    """IDs for cups"""
    EC = 424
    """European Championships France 2016"""
    DFB = 432
    """DFB-Pokal 2016/17"""
    CL = 440
    """Champions League 2016/17"""


class LeagueId(CompetitionId):
    """IDs for leagues"""
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
    league = models.CharField(
        max_length=255,
        choices=((subclass.choices()[0], subclass.choices()[1]) for subclass in CompetitionId.__subclasses__())
    )
    year = models.IntegerField(choices=[(r, r) for r in range(1980, (datetime.datetime.now().year + 1))])
    current_matchday = models.PositiveSmallIntegerField()
    number_of_matchdays = models.PositiveSmallIntegerField()
    number_of_teams = models.PositiveSmallIntegerField()
    number_of_games = models.PositiveSmallIntegerField()
    last_updated = models.DateTimeField()

    class Meta:
        ordering = ['caption']

    def is_last_matchday(self):
        return self.current_matchday == self.number_of_matchdays
