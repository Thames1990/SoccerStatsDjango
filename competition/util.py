def fetch_competitions(competition_id=None):
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


def get_or_create_competition(competition):
    """
    Gets Competition object from the database if it already exists or creates it from JSON.
    :param competition: JSON representation
    :return: Competition object generated or fetched from database
    """
    from competition.models import Competition
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


def get_or_create_competitions(competition_id=None):
    """
    Gets Competition objects from the database if they already exists or create them from JSON.
    :param competition_id: Id of a Competition. If None, all Competition objects are handled.
    :return: A Competition object defined by its id, if competition_id was specified; all Competition objects from
    the database otherwise.
    """
    if competition_id:
        return get_or_create_competition(fetch_competitions(competition_id))
    else:
        competitions = []
        for competition in fetch_competitions():
            competitions.append(get_or_create_competition(competition))
        return competitions
