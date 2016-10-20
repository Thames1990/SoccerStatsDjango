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
    from competition.models import Competition
    Competition.objects.get_or_create(
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


def get_or_create_competitions(competition_id=None):
    if competition_id:
        get_or_create_competition(fetch_competitions(competition_id))
    else:
        for competition in fetch_competitions():
            get_or_create_competition(competition)
