import logging

from django.utils.dateparse import parse_datetime

from SoccerStats.utils import timing, rate_limited
from competition.models import Competition
from table.utils import fetch_table

logger = logging.getLogger(__name__)


@rate_limited(0.8)
def fetch_competition(competition_id=None, season=None):
    """
    Fetches JSON representation of competitions from football-data.org.
    Fetches a single competition if competition_id is specified, all competitions otherwise.
    :param competition_id: Id of a competition
    :param season: Year of a season
    :return: JSON representation of a competition or all competitions
    """
    import requests

    base_url = 'http://api.football-data.org/v1/competitions/'
    if competition_id:
        base_url += str(competition_id)
    if season:
        base_url += '?season=' + str(season)

    return requests.get(
        url=base_url,
        headers={'X-Auth-Token': 'bf0513ea0ba6457fb4ae6d380cca8365'}
    ).json()


def fetch_competitions():
    """
    Fetches all available competitions from every season documented at football-data.org.
    :return: List of JSON representation of all available competitions
    """
    from datetime import datetime

    competitions = []

    for season in range(2015, datetime.today().year + 1):
        for competition in fetch_competition(season=season):
            if 'error' in competition:
                logger.warning('Competitions for season ' + str(season) + ' aren\'t available')
                break
            competitions.append(competition)

    return competitions


@timing
def create_competitions():
    """
    Creates all competitions.
    :return: Created Competition objects
    """
    logger.info('Creating competitions...')

    competitions = []

    for competition in fetch_competitions():
        competitions.append(
            Competition(
                id=int(competition['id']),
                is_cup='standings' in fetch_table(competiton_id=competition['id']),
                caption=competition['caption'],
                league=competition['league'],
                year=int(competition['year']),
                current_matchday=int(competition['currentMatchday']),
                number_of_matchdays=int(competition['numberOfMatchdays']),
                number_of_teams=int(competition['numberOfTeams']),
                number_of_games=int(competition['numberOfGames']),
                last_updated=parse_datetime(competition['lastUpdated']),
            )
        )

    created_competitions = Competition.objects.bulk_create(competitions)
    logger.info('Created ' + str(len(created_competitions)) + ' competitions')
    return created_competitions


@timing
def update_competitions():
    """
    Updates all competitions. Updates the fields, if a matching competition already exists
    ; creates a new competition otherwise.
    :return: List of updated competitions
    """
    logger.info('Updating competitions...')

    updated_competitions = []
    created_competitions = 0

    for competition in fetch_competitions():
        competition_object, created = Competition.objects.update_or_create(
            id=competition['id'],
            defaults={
                'id': int(competition['id']),
                'is_cup': 'standings' in fetch_table(competiton_id=competition['id']),
                'caption': competition['caption'],
                'league': competition['league'],
                'year': int(competition['year']),
                'current_matchday': int(competition['currentMatchday']),
                'number_of_matchdays': int(competition['numberOfMatchdays']),
                'number_of_teams': int(competition['numberOfTeams']),
                'number_of_games': int(competition['numberOfGames']),
                'last_updated': parse_datetime(competition['lastUpdated']),
            }
        )

        # TODO Use *last_updated* to update tables

        if created:
            created_competitions += 1
        else:
            updated_competitions.append(competition_object)

    logger.info('Updated ' + str(len(updated_competitions)) + ' competitions, created ' + str(created_competitions))
    return updated_competitions
