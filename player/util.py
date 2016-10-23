import requests


def get_player_image(player):
    """
    Gets the Wikipedia page image for a player
    :param player: Player, whose image to look for
    :return: URL to the Wikimedia player image if it exists; None otherwise
    """
    json = requests.get('http://en.wikipedia.org/w/api.php', {
        'action': 'query',
        'format': 'json',
        'generator': 'search',
        'gsrsearch': player['name'],
        'gsrlimit': 1,
        'prop': 'pageimages',
        'piprop': 'thumbnail',
        'pilimit': 'max',
        'pithumbsize': 400
    }).json()
    try:
        return list(json['query']['pages'].values())[0]['thumbnail']['source']
    except KeyError:
        # TODO Implement different image provider
        # TODO Change to logging
        print('Picture for ' + player['name'] + ' not found.')


def fetch_players(team_id):
    return requests.get(
        'http://api.football-data.org/v1/teams/' + str(team_id) + '/players',
        headers={'X-Auth-Token': 'bf0513ea0ba6457fb4ae6d380cca8365'}
    ).json()['players']


def get_players(team_id):
    players = []
    for player in fetch_players(team_id):
        from player.models import Player
        from team.models import Team
        import re

        players.append(
            Player.objects.get_or_create(
                team=Team.objects.get(id=team_id),
                name=player['name'],
                position=dict(Player.POSITION)[player['position']],
                jersey_number=player['jerseyNumber'],
                date_of_birth=player['dateOfBirth'],
                nationality=player['nationality'],
                contract_until=player['contractUntil'],
                market_value=re.sub('[^0-9]', '', player['marketValue']) if player['marketValue'] else None,
                image=get_player_image(player),
            )[0]
        )
    return players


def get_all_players():
    from team.models import Team

    players = []
    for team in Team.objects.all():
        players.append(get_players(team.id))
    return players
