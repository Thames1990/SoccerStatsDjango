import re

from competition.models import Competition
from SoccerStats.utils import timing
from team.models import Team


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


def create_team(team):
    """
    Creates a Team object.
    :param team: JSON representation of a team
    :return: Created Team object
    """
    return Team(
        id=re.sub('[^0-9]', '', team['_links']['self']['href'])[1:],
        name=team['name'],
        code=team['code'] or None,
        short_name=team['shortName'],
        squad_market_value=re.sub('[^0-9]', '', team['squadMarketValue']) if team['squadMarketValue'] else None,
        # TODO Add image check and fallback download from wikipedia
        crest_url=team['crestUrl'],
    )


@timing
def create_teams():
    """Creates all teams."""
    # TODO Fix this shit
    for competition in Competition.objects.all():
        for team in fetch_teams(competition.id):
            team_object = create_team(team)
            team_object.save()
            team_object.competition.add(competition)


@timing
def update_teams():
    """Updates all teams."""
    for competition in Competition.objects.all():
        for team in fetch_teams(competition['id']):
            Team.objects.filter(
                id=re.sub('[^0-9]', '', team['_links']['self']['href'])[1:]
            ).update(
                name=team['name'],
                code=team['code'] if team['code'] else None,
                short_name=team['shortName'],
                squad_market_value=re.sub('[^0-9]', '', team['squadMarketValue']) if team['squadMarketValue'] else None,
                # TODO Add image check and fallback download from wikipedia
                crest_url=team['crestUrl'],
            )
