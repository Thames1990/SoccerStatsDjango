from competition.models import Competition


def fetch_competitions(competition_id=None):
    """
    Fetches JSON representation of competitions from football-data.org.
    Fetches a single competition if competition_id is specified, all competitions otherwise.
    :param competition_id: Id of a competition
    :return: JSON representation of a competition or all competitions
    """
    import requests

    base_url = 'http://api.football-data.org/v1/competitions/'
    if competition_id:
        base_url += str(competition_id)

    return requests.get(
        url=base_url,
        headers={'X-Auth-Token': 'bf0513ea0ba6457fb4ae6d380cca8365'}
    ).json()


def create_competition(competition):
    """
    Creates a Competition object.
    :param competition: JSON representation of the competition
    :return: Competition object
    """
    return Competition(
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


def create_all_competitions():
    """Creates all competitions in the database."""
    competitions = []
    for competition in fetch_competitions():
        competitions.append(create_competition(competition))

    Competition.objects.bulk_create(objs=competitions)


def update_all_competitions():
    """Updates all competitions in the database"""
    # TODO Check update_or_create
    # TODO Rewrite all util functions for each app
    for competition in fetch_competitions():
        Competition.objects.filter(id=competition['id']).update(
            caption=competition['caption'],
            league=competition['league'],
            year=competition['year'],
            current_matchday=competition['currentMatchday'],
            number_of_matchdays=competition['numberOfMatchdays'],
            number_of_teams=competition['numberOfTeams'],
            number_of_games=competition['numberOfGames'],
            last_updated=competition['lastUpdated'],
        )
