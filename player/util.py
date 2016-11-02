import re
import requests

from player.models import Player
from team.models import Team


def get_player_image(player_name):
    """
    Gets the Wikipedia page image for a player
    :param player_name: Player, whose image to look for
    :return: URL to the Wikimedia player image if it exists; None otherwise
    """
    json = requests.get(
        url='http://en.wikipedia.org/w/api.php',
        params={
            'action': 'query',
            'format': 'json',
            'generator': 'search',
            'gsrsearch': player_name,
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
        pass


def fetch_players(team_id):
    """
    Fetches JSON representation of players from football-data.org.
    :param team_id: Id of a team
    :return: JSON representation of players from a team
    """
    try:
        return requests.get(
            url='http://api.football-data.org/v1/teams/' + str(team_id) + '/players',
            headers={'X-Auth-Token': 'bf0513ea0ba6457fb4ae6d380cca8365'}
        ).json()['players']
    except KeyError:
        # TODO Log teams without players
        # Return empty dictionary for iterable loop check
        return {}


def create_player(player, team_id):
    """
    Creates a player.
    :param player: JSON representation of a player
    :param team_id: Id of a team
    :return: Created player
    """
    return Player(
        team=Team.objects.get(id=team_id),
        name=player['name'],
        position=dict(Player.POSITION)[player['position']],
        jersey_number=player['jerseyNumber'],
        date_of_birth=player['dateOfBirth'] if player['dateOfBirth'] else None,
        nationality=dict(Player.NATION)[player['nationality']],
        contract_until=player['contractUntil'],
        market_value=re.sub('[^0-9]', '', player['marketValue']) if player['marketValue'] else None,
        image=get_player_image(player['name']),
    )


def create_players(team_id):
    """
    Creates player from a team.
    :param team_id: Id of the team
    :return: Created players
    """
    players = []
    for player in fetch_players(team_id):
        # Empty players indicate an empty player list
        if not player:
            break
        players.append(create_player(player, team_id))
    return players


def create_all_players():
    """
    Creates all players.
    :return: Created players
    """
    players = []
    for team in Team.objects.all():
        players.extend(create_players(team.id))
    return players


def update_player(player, team_id):
    """
    Updates a player.
    :param player: JSON representation of the player to be updated
    :param team_id: Id of the players team
    :return: Number of updated rows
    """
    name = player['name']
    return Player.objects.filter(
        name=name,
        date_of_birth=player['dateOfBirth'],
    ).update(
        team=Team.objects.get(id=team_id),
        position=dict(Player.POSITION)[player['position']],
        jersey_number=player['jerseyNumber'],
        contract_until=player['contractUntil'],
        market_value=re.sub('[^0-9]', '', player['marketValue']) if player['marketValue'] else None,
        image=get_player_image(player['name']),
    )


def update_players(team_id):
    """
    Updates all players of a team.
    :param team_id: Id of the team
    :return: Number of updated rows
    """
    updated_rows = 0
    for player in fetch_players(team_id):
        updated_rows += update_player(player, team_id)
    return updated_rows


def update_all_players():
    """
    Updates all players.
    :return: Number of updated rows
    """
    updated_rows = 0
    for team in Team.objects.all():
        update_players(team.id)
    return updated_rows
