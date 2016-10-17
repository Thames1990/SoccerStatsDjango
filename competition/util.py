import re

from competition.models import Competition


def fetch_competitions(competition_id):
    """
    Fetches a competition if competition_id is not None; fetches all competitions otherwise
    :param competition_id: Integer id of competition or None
    :return: JSON representation of a competition or all competitions
    """
    import requests
    base_url = 'http://api.football-data.org/v1/competitions/'
    if competition_id:
        base_url += str(competition_id)
    return requests.get(
        base_url,
        headers={'X-Auth-Token': 'bf0513ea0ba6457fb4ae6d380cca8365'}
    ).json()


def fetch_cup_ids():
    """
    Fetches all cup ids
    :return: List of all cup ids
    """
    cup_ids = []
    for competition in fetch_competitions(None):
        if int(competition['numberOfGames']) < 100:
            cup_ids.append(competition['id'])
    return cup_ids


def fetch_league_ids():
    """
    Fetches all league ids
    :return: List of all league ids
    """
    league_ids = []
    for competition in fetch_competitions(None):
        if int(competition['numberOfGames']) >= 100:
            league_ids.append(competition['id'])
    return league_ids


def fetch_cup_names():
    """
    Fetches all cup names
    :return: List of all cup names
    """
    cup_ids = []
    for competition in fetch_competitions(None):
        if int(competition['numberOfGames']) < 100:
            cup_ids.append(re.sub('[^a-zA-Z\s]+', '', competition['caption']))
    return cup_ids


def fetch_league_names():
    """
    Fetches all league names
    :return: List of all league names
    """
    league_ids = []
    for competition in fetch_competitions(None):
        if int(competition['numberOfGames']) >= 100:
            league_ids.append(re.sub('[^a-zA-Z\s]+', '', competition['caption']))
    return league_ids


def get_or_create_competition(competition):
    return Competition.objects.get_or_create(
        id=competition['id'],
        caption=competition['caption'],
        league=competition['league'],
        year=competition['year'],
        current_matchday=competition['currentMatchday'],
        number_of_matchdays=competition['numberOfMatchdays'],
        number_of_teams=competition['numberOfTeams'],
        number_of_games=competition['numberOfGames'],
        last_updated=competition['lastUpdated'],
    )[0]


def get_or_create_competitions(competition_id):
    competitions = fetch_competitions(competition_id)
    if competition_id:
        return get_or_create_competition(competitions)
    else:
        competition_list = []
        for competition in competitions:
            competition_list.append(get_or_create_competition(competition))
        return competition_list
