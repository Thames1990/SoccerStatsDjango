from competition.util import get_league_ids, get_cup_ids


def get_teams(competition_id):
    import requests
    return requests.get(
        'http://api.football-data.org/v1/competitions/' + competition_id + '/teams',
        headers={'X-Auth-Token': 'bf0513ea0ba6457fb4ae6d380cca8365'}
    ).json()


def get_team_ids():
    import re
    team_ids = []
    for competition_id in {**get_cup_ids(), **get_league_ids()}.values():
        team = get_teams(str(competition_id))['_links']['self']['href']
        team_ids.append(int(re.sub('[^0-9]', '', team)[1:]))
    return team_ids
