import requests

from .models import LeagueTable, Standing, Home, Away


def get_league_table(url):
    json = requests.get(url, headers={'X-Auth-Token': 'bf0513ea0ba6457fb4ae6d380cca8365'}).json()

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
