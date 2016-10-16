def get_competitions():
    import requests
    return requests.get(
        'http://api.football-data.org/v1/competitions',
        headers={'X-Auth-Token': 'bf0513ea0ba6457fb4ae6d380cca8365'}
    ).json()


def get_cup_ids():
    cup_ids = {}
    for competition in get_competitions():
        if int(competition['numberOfGames']) < 100:
            cup_ids.update({competition['league']: competition['id']})
    return cup_ids


def get_league_ids():
    league_ids = {}
    for competition in get_competitions():
        if int(competition['numberOfGames']) >= 100:
            league_ids.update({competition['league']: competition['id']})
    return league_ids
