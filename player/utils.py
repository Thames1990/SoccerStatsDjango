import re
import requests

from SoccerStats.utils import timing, rate_limited
from player.models import Player
from team.models import Team


def get_player_image(player_name):
    """
    Gets the Wikipedia page image for a player with name *player_name*
    :param player_name: Player, whose image to look for
    :return: URL to the Wikimedia player image if it exists; None otherwise
    """
    json = requests.get(
        url='https://en.wikipedia.org/w/api.php',
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
        return None


@rate_limited(0.8)
def fetch_players(team_id):
    """
    Fetches JSON representation of players from football-data.org.
    :param team_id: Id of a team
    :return: JSON representation of players from a team with id *team_id* if players exist; *None* otherwise
    """
    json = requests.get(
        url='http://api.football-data.org/v1/teams/' + str(team_id) + '/players',
        headers={'X-Auth-Token': 'bf0513ea0ba6457fb4ae6d380cca8365'}
    ).json()
    return json['players'] if 'players' in json else None


def create_player(team, player):
    """
    Creates a player.
    :param team: JSON representation of the player's team
    :param player: JSON representation of the player
    :return:
    """
    return Player(
        team=team,
        name=player['name'],
        position=player['position'],
        jersey_number=player['jerseyNumber'],
        date_of_birth=player['dateOfBirth'] if player['dateOfBirth'] else None,
        nationality=player['nationality'],
        contract_until=player['contractUntil'],
        market_value=re.sub('[^0-9]', '', player['marketValue']) if player['marketValue'] else None,
        image=get_player_image(player['name']),
    )


@timing
def create_players():
    """
    Creates all players.
    :return: Created players
    """
    player_objects = []

    for team in Team.objects.all():
        players = fetch_players(team.id)
        if players:
            for player in players:
                player_objects.append(create_player(team, player))

    return Player.objects.bulk_create(player_objects)


@timing
def update_players():
    """Updates all players."""
    for team in Team.objects.all():
        for player in fetch_players(team.id):
            Player.objects.filter(
                name=player['name'],
                date_of_birth=player['dateOfBirth'],
            ).update(
                team=team,
                position=player['position'],
                jersey_number=player['jerseyNumber'],
                contract_until=player['contractUntil'],
                market_value=re.sub('[^0-9]', '', player['marketValue']) if player['marketValue'] else None,
                image=get_player_image(player['name']),
            )
