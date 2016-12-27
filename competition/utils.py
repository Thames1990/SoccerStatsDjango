import logging

from competition.models import Competition

from SoccerStats.utils import timing

logger = logging.getLogger(__name__)


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
    from table.utils import fetch_tables

    competitions = []

    for competition in fetch_competitions():
        competitions.append(
            Competition(
                id=competition['id'],
                is_cup='standings' in fetch_tables(competiton_id=competition['id']),
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
    """Updates all competitions."""
    for competition_id in fetch_competitions():
        competition = fetch_competition(competition_id=competition_id)
        Competition.objects.filter(
            id=competition['id']
        ).update(
            current_matchday=competition['currentMatchday'],
            last_updated=competition['lastUpdated'],
        )
