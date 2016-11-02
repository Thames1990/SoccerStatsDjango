import re

from competition.models import Competition
from team.models import Team

from competition.util import fetch_competitions


def fetch_teams(competition_id):
    """
    Fetches JSON representation of teams from football-data.org.
    :param competition_id: Id of a competition
    :return: JSON representation of a teams from a competition
    """
    import requests

    return requests.get(
        url='http://api.football-data.org/v1/competitions/' + str(competition_id) + '/teams',
        headers={'X-Auth-Token': 'bf0513ea0ba6457fb4ae6d380cca8365'}
    ).json()['teams']


def create_team(team, competition_id):
    """
    Creates a team.
    :param team: Team to be created
    :param competition_id: Id of the competition of the team
    :return: Created team
    """
    Team(
        id=re.sub('[^0-9]', '', team['_links']['self']['href'])[1:],
        name=team['name'],
        code=team['code'] if team['code'] else None,
        short_name=team['shortName'],
        squad_market_value=re.sub('[^0-9]', '', team['squadMarketValue']) if team['squadMarketValue'] else None,
        crest_url=team['crestUrl']  # TODO Add image check and fallback download from wikipedia
    )
    team.competition.add(Competition.objects.get(id=competition_id))
    return team


def create_teams(competition_id):
    """
    Creates teams of a specific competition.
    :param competition_id: Id of the competition
    :return: Created teams
    """
    teams = []

    for team in fetch_teams(competition_id):
        teams.append(create_team(team, competition_id))

    return teams


def create_all_teams():
    """
    Creates all teams.
    :return: Created teams
    """
    teams = []
    for competition in Competition.objects.all():
        teams.extend(create_teams(competition.id))

    return Team.objects.bulk_create(teams)


def update_team(team):
    """
    Updates a team.
    :param team: Team to be updated
    :return: Number of updated rows
    """
    # TODO update competitions
    return Team.objects.filter(id=re.sub('[^0-9]', '', team['_links']['self']['href'])[1:]).update(
        name=team['name'],
        code=team['code'] if team['code'] else None,
        short_name=team['shortName'],
        squad_market_value=re.sub('[^0-9]', '', team['squadMarketValue']) if team['squadMarketValue'] else None,
        crest_url=team['crestUrl'],
    )


def update_teams(competition_id):
    """
    Updates teams of a specific competition.
    :param competition_id: Id of the competition
    :return: Number of updated rows
    """
    updated_rows = 0
    for team in fetch_teams(competition_id):
        updated_rows += update_team(team)
    return updated_rows


def update_all_teams():
    """
    Updates all teams.
    :return: Number of updated rows
    """
    updated_rows = 0
    for competition in fetch_competitions():
        updated_rows += update_teams(competition['id'])
    return updated_rows
