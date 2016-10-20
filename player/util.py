import requests


def get_player_image(player):
    """
    Gets the Wikipedia page image for a player
    :param player: Player, whose image to look for
    :return: URL to the Wikimedia player image if it exists; None otherwise
    """
    json = requests.get('http://de.wikipedia.org/w/api.php', {
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
        print('Picture for ' + player['name'] + ' not found.')


def create_or_get_player(player, team_id):
    """
    Creates a player from JSON provided by football-data.org if he didn't exist in the database; gets the player from
    the database otherwise
    :param player: JSON representation for a player
    :param team_id: Id of the players team
    :return: Player object
    """
    from player.models import Player
    from team.models import Team
    import re

    return Player.objects.get_or_create(
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


def fetch_team_players(team_id):
    """
    Gets the JSON representation for a team
    :param team_id: ID of a team
    :return: JSON representation for a team
    """
    return requests.get(
        'http://api.football-data.org/v1/teams/' + str(team_id) + '/players',
        headers={'X-Auth-Token': 'bf0513ea0ba6457fb4ae6d380cca8365'}
    ).json()['players']


def get_player(team_id, name):
    """
    Gets a player
    :param team_id: ID of the players team
    :param name: Name of the player
    :return: Player object if the player exists in the team; None otherwise
    """
    for player in fetch_team_players(team_id):
        if player['name'].replace(' ', '-').lower() == name.replace('%20', '-').replace(' ', '-').lower():
            return create_or_get_player(player, team_id)


def get_players(team_id):
    """
    Gets all players of a team
    :param team_id: ID of the team
    :return: List of Player objects
    """
    players = []
    for player in fetch_team_players(team_id):
        players.append(create_or_get_player(player, team_id))
    return players


def get_all_players():
    from team.models import Team
    for team in Team.objects.all():
        get_players(team.id)
