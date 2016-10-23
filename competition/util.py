def fetch_competitions(competition_id=None):
    import requests

    base_url = 'http://api.football-data.org/v1/competitions/'
    if competition_id:
        base_url += str(competition_id)
    return requests.get(
        base_url,
        headers={'X-Auth-Token': 'bf0513ea0ba6457fb4ae6d380cca8365'}
    ).json()


def get_competition(competition_id):
    from competition.models import Competition

    competition = fetch_competitions(competition_id)
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


def get_all_competitions():
    for competition in fetch_competitions():
        get_competition(competition['id'])
