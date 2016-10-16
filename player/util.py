import re
import requests

from player.models import Player


def get_player_image(player):
    """
    Gets the Wikipedia page image for a player
    :param player: Player, whose image to look for
    :return: URL to the Wikimedia player image if it exists; None otherwise
    """
    image_field = list(requests.get('http://de.wikipedia.org/w/api.php', {
        'action': 'query',
        'format': 'json',
        'generator': 'search',
        'gsrsearch': player['name'],
        'gsrlimit': 1,
        'prop': 'pageimages',
        'piprop': 'thumbnail',
        'pilimit': 'max',
        'pithumbsize': 400
    }).json()['query']['pages'].values())[0]
    if 'thumbnail' in image_field:
        return image_field['thumbnail']['source']
    return None


def get_team(team_id):
    """
    Gets the JSON representation for a team
    :param team_id: ID of a team
    :return: JSON representation for a team
    """
    return requests.get(
        'http://api.football-data.org/v1/teams/' + str(team_id) + '/players',
        headers={'X-Auth-Token': 'bf0513ea0ba6457fb4ae6d380cca8365'}
    ).json()


def create_or_get_player(player):
    """
    Creates a player from JSON provided by football-data.org if he didn't exist in the database; gets the player from
    the database otherwise
    :param player: JSON representation for a player
    :return: Player object
    """
    return Player.objects.get_or_create(
        name=player['name'],
        position=player['position'],
        jersey_number=player['jerseyNumber'],
        date_of_birth=player['dateOfBirth'],
        nationality=player['nationality'],
        contract_until=player['contractUntil'],
        market_value=re.sub('[^0-9]', '', player['marketValue']),
        image=get_player_image(player),
    )[0]


def get_players(team_id):
    """
    Gets all players of a team
    :param team_id: ID of the team
    :return: List of Player objects
    """
    players = []
    for player in get_team(team_id)['players']:
        players.append(create_or_get_player(player))
    return players


def get_player(team_id, name):
    """
    Gets a player
    :param team_id: ID of the players team
    :param name: Name of the player
    :return: Player object if the player exists in the team; None otherwise
    """
    for player in get_team(team_id)['players']:
        if player['name'].replace(' ', '-').lower() == name:
            return create_or_get_player(player)
