import logging
import re

from competition.models import Competition
from SoccerStats.utils import timing
from team.models import Team

logger = logging.getLogger(__name__)


def fetch_teams(competition_id):
    """
    Fetches JSON representation of teams from football-data.org.
    :param competition_id: Id of a competition
    :return: JSON representation of a teams from a competition
    """
    import requests

    return requests.get(
        url='https://api.football-data.org/v1/competitions/' + str(competition_id) + '/teams',
        headers={'X-Auth-Token': 'bf0513ea0ba6457fb4ae6d380cca8365'},
    ).json()['teams']


@timing
def create_teams():
    """
    Creates all team.
    :return: List of created teams
    """
    logger.info('Creating teams...')

    created_teams = []

    for competition in Competition.objects.all():
        for team in fetch_teams(competition.id):
            # teams might already be created in another competition
            team_object, created = Team.objects.get_or_create(
                id=re.sub('[^0-9]', '', team['_links']['self']['href'])[1:],
                name=team['name'],
                code=team['code'] or None,
                short_name=team['shortName'],
                squad_market_value=re.sub('[^0-9]', '', team['squadMarketValue']) if team['squadMarketValue'] else None,
                # TODO Add image check and fallback download from wikipedia
                crest_url=team['crestUrl'],
            )
            # TODO Optimize with bulk_create and ThroughModel
            team_object.competition.add(competition)
            if created:
                created_teams.append(team_object)

    logger.info('Created ' + str(len(created_teams)) + ' teams')
    return created_teams


@timing
def update_teams():
    """
    Updates all teams. Updates the fields, if a matching team already exists; creates a new team otherwise.
    :return: List of updated teams
    """
    logger.info('Updating teams...')

    updated_teams = []
    created_teams = 0

    for competition in Competition.objects.all():
        for team in fetch_teams(competition.id):
            team_object, created = Team.objects.update_or_create(
                id=re.sub('[^0-9]', '', team['_links']['self']['href'])[1:],
                defaults={
                    'id': re.sub('[^0-9]', '', team['_links']['self']['href'])[1:],
                    'name': team['name'],
                    'code': team['code'] or None,
                    'short_name': team['shortName'],
                    'squad_market_value': re.sub(
                        '[^0-9]', '', team['squadMarketValue']
                    ) if team['squadMarketValue'] else None,
                    # TODO Add image check and fallback download from wikipedia
                    'crest_url': team['crestUrl'],
                }
            )

            created_teams += 1 if created else updated_teams.append(team_object)

    logger.info('Updated ' + str(len(updated_teams)) + ' teams, created ' + str(created_teams))
    return updated_teams


def get_squad_market_value_average():
    """
    Calculates the average squad market value.
    :return: Average squad market value
    """
    squad_market_value_average = 0
    teams = 0
    for team in Team.objects.all():
        squad_market_value_average += team.get_squad_market_value()
        teams += 1
    # Division by zero
    if teams:
        return squad_market_value_average / teams
    else:
        return 0
