import requests
from enum import Enum
import logging

from .models import LeagueTable, Standing, Home, Away


class CupID(Enum):
    EC = 424
    """European Championships France 2016"""
    DFB = 432
    """DFB-Pokal 2016/17"""
    CL = 440
    """Champions League 2016/17"""


class LeagueID(Enum):
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


def get_league_table(league_id):
    if isinstance(league_id, LeagueID):
        json = requests.get(
            'http://api.football-data.org/v1/competitions/' + str(league_id.value) + '/leagueTable',
            headers={'X-Auth-Token': 'bf0513ea0ba6457fb4ae6d380cca8365'}
        ).json()

        league_table, created = LeagueTable.objects.get_or_create(
            league_caption=json['leagueCaption'],
            matchday=json['matchday'],
        )

        for team in json['standing']:
            standing, created = Standing.objects.get_or_create(
                league_table=league_table,
                position=team['position'],
                team_name=team['teamName'],
                crest_uri=team['crestURI'],
                played_games=team['playedGames'],
                points=team['points'],
                goals=team['goals'],
                goals_against=team['goalsAgainst'],
                goal_difference=team['goalDifference'],
                wins=team['wins'],
                draws=team['draws'],
                losses=team['losses']
            )

            Home.objects.get_or_create(
                standing=standing,
                goals=team['home']['goals'],
                goals_against=team['home']['goalsAgainst'],
                wins=team['home']['wins'],
                draws=team['home']['draws'],
                losses=team['home']['losses']
            )

            Away.objects.get_or_create(
                standing=standing,
                goals=team['away']['goals'],
                goals_against=team['home']['goalsAgainst'],
                wins=team['away']['wins'],
                draws=team['away']['draws'],
                losses=team['away']['losses']
            )

        return league_table
    else:
        return NotImplemented
