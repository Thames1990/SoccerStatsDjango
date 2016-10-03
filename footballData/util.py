import requests

from .models import LeagueTable, Standing, Home, Away


def get_league_table(url):
    json = requests.get(url).json()

    home = Home.objects.create(
        goals=int(json['standing'][0]['home']['goals']),
        goalsAgainst=int(json['standing'][0]['home']['goalsAgainst']),
        wins=int(json['standing'][0]['home']['wins']),
        draws=int(json['standing'][0]['home']['draws']),
        losses=int(json['standing'][0]['home']['losses'])
    )

    away = Away.objects.create(
        goals=int(json['standing'][0]['away']['goals']),
        goalsAgainst=int(json['standing'][0]['home']['goalsAgainst']),
        wins=int(json['standing'][0]['away']['wins']),
        draws=int(json['standing'][0]['away']['draws']),
        losses=int(json['standing'][0]['away']['losses'])
    )

    standing = Standing.objects.create(
        position=int(json['standing'][0]['position']),
        teamName=json['standing'][0]['teamName'],
        crestURI=json['standing'][0]['crestURI'],
        playedGames=int(json['standing'][0]['playedGames']),
        points=int(json['standing'][0]['points']),
        goals=int(json['standing'][0]['goals']),
        goalsAgainst=int(json['standing'][0]['goalsAgainst']),
        goalDifference=int(json['standing'][0]['goalDifference']),
        wins=int(json['standing'][0]['wins']),
        draws=int(json['standing'][0]['draws']),
        losses=int(json['standing'][0]['losses']),
        home=home,
        away=away
    )

    return LeagueTable.objects.create(
        leagueCaption=json['leagueCaption'],
        matchday=int(json['matchday']),
        standing=standing
    )
