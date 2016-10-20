import re
import requests

from .models import Team


def get_or_create_team(team_id):
    team = requests.get(
        'http://api.football-data.org/v1/teams/' + str(team_id),
        headers={'X-Auth-Token': 'bf0513ea0ba6457fb4ae6d380cca8365'}
    ).json()

    Team.objects.get_or_create(
        id=re.sub('[^0-9]', '', team['_links']['self']['href'])[1:],
        name=team['name'],
        code=team['code'],
        short_name=team['shortName'],
        squad_market_value=re.sub('[^0-9]', '', team['squadMarketValue']),
        crest_url=team['crestUrl']
    )


def get_or_create_competition_teams(competition_id):
    teams = requests.get(
        'http://api.football-data.org/v1/competitions/' + str(competition_id) + '/teams',
        headers={'X-Auth-Token': 'bf0513ea0ba6457fb4ae6d380cca8365'}
    ).json()['teams']

    for team in teams:
        Team.objects.get_or_create(
            id=re.sub('[^0-9]', '', team['_links']['self']['href'])[1:],
            name=team['name'],
            code=team['code'],
            short_name=team['shortName'],
            squad_market_value=re.sub('[^0-9]', '', team['squadMarketValue']),
            crest_url=team['crestUrl']
        )


def get_or_create_all_teams():
    from competition.util import fetch_cup_ids, fetch_league_ids
    for competition_id in {**fetch_cup_ids(), **fetch_league_ids()}.values():
        get_or_create_competition_teams(competition_id)
