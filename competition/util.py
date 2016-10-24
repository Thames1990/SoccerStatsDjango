from competition.models import Competition


def fetch_competitions(competition_id=None):
    import requests

    base_url = 'http://api.football-data.org/v1/competitions/'
    if competition_id:
        base_url += str(competition_id)
    return requests.get(
        base_url,
        headers={'X-Auth-Token': 'bf0513ea0ba6457fb4ae6d380cca8365'}
    ).json()


def create_competition(competition):
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
    competitions = []
    for competition in fetch_competitions():
        competitions.append(create_competition(competition))

    Competition.objects.bulk_create(competitions)
