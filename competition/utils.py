import logging

from SoccerStats.utils import timing
from competition.models import Competition

logger = logging.getLogger(__name__)


def fetch_competitions(competition_id=None, season=None):
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


def fetch_competition_ids():
    """
    Fetches ids of all available competitions from every season documented at football-data.org.
    :return: List of ids of available competitions
    """
    from datetime import datetime
    competition_ids = []
    for season in range(2015, datetime.today().year + 1):
        for competition in fetch_competitions(season=season):
            if 'error' in competition:
                logger.warning('Competitions for season ' + str(season) + ' aren\'t available')
                break
            competition_ids.append(competition['id'])
    return competition_ids


@timing
def create_competitions():
    """
    Creates all competitions.
    :return: Created competitions
    """
    competitions = []

    for competition_id in fetch_competition_ids():
        competition = fetch_competitions(competition_id=competition_id)
        competitions.append(
            Competition(
                id=competition['id'],
                caption=competition['caption'],
                league=competition['league'],
                year=competition['year'],
                current_matchday=competition['currentMatchday'],
                number_of_matchdays=competition['numberOfMatchdays'],
                number_of_teams=competition['numberOfTeams'],
                number_of_games=competition['numberOfGames'],
                last_updated=competition['lastUpdated'],
            )
        )

    return Competition.objects.bulk_create(competitions)


@timing
def update_competitions():
    """
    Updates all competitions.
    :return: Number of updated rows
    """
    updated_rows = 0

    for competition_id in fetch_competition_ids():
        competition = fetch_competitions(competition_id=competition_id)
        updated_rows += Competition.objects.filter(id=competition['id']).update(
            caption=competition['caption'],
            league=competition['league'],
            year=competition['year'],
            current_matchday=competition['currentMatchday'],
            number_of_matchdays=competition['numberOfMatchdays'],
            number_of_teams=competition['numberOfTeams'],
            number_of_games=competition['numberOfGames'],
            last_updated=competition['lastUpdated'],
        )

    return updated_rows
