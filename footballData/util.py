import requests

from .models import LeagueTable, Standing, Home, Away


def get_league_table(url):
    json = requests.get(url).json()

    league_table = LeagueTable.objects.create(
        league_caption=json['leagueCaption'],
        matchday=int(json['matchday']),
    )

    for team in json['standing']:
        standing = Standing.objects.create(
            league_table=league_table,
            position=int(team['position']),
            team_name=team['teamName'],
            crest_uri=team['crestURI'],
            played_games=int(team['playedGames']),
            points=int(team['points']),
            goals=int(team['goals']),
            goals_against=int(team['goalsAgainst']),
            goal_difference=int(team['goalDifference']),
            wins=int(team['wins']),
            draws=int(team['draws']),
            losses=int(team['losses'])
        )

        Home.objects.create(
            standing=standing,
            goals=int(team['home']['goals']),
            goals_against=int(team['home']['goalsAgainst']),
            wins=int(team['home']['wins']),
            draws=int(team['home']['draws']),
            losses=int(team['home']['losses'])
        )

        Away.objects.create(
            standing=standing,
            goals=int(team['away']['goals']),
            goals_against=int(team['home']['goalsAgainst']),
            wins=int(team['away']['wins']),
            draws=int(team['away']['draws']),
            losses=int(team['away']['losses'])
        )

    return league_table
