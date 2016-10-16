import requests
import logging

from player.models import Player


def get_player_image(player):
    baseurl = 'http://de.wikipedia.org/w/api.php'
    attr = {
        'action': 'query',
        'format': 'json',
        'generator': 'search',
        'gsrsearch': player['name'],
        'gsrlimit': 1,
        'prop': 'pageimages',
        'piprop': 'thumbnail',
        'pilimit': 'max',
        'pithumbsize': 400
    }
    json = requests.get(baseurl, params=attr).json()
    # TODO Fix weird KeyError 0
    # TODO Fix DisambiguationError
    image_field = json['query']['pages'].get(next(json['query']['pages'].__iter__()))
    if 'thumbnail' in image_field:
        return image_field['thumbnail']['source']
    else:
        logging.error(player['name'] + ' image not found in: ' + str(image_field))
        return None


def get_players(team_id):
    json = requests.get(
        'http://api.football-data.org/v1/teams/' + str(team_id) + '/players',
        headers={'X-Auth-Token': 'bf0513ea0ba6457fb4ae6d380cca8365'}
    ).json()

    players = []
    for player in json['players']:
        player, created = Player.objects.get_or_create(
            name=player['name'],
            position=player['position'],
            jersey_number=player['jerseyNumber'],
            date_of_birth=player['dateOfBirth'],
            nationality=player['nationality'],
            contract_until=player['contractUntil'],
            market_value=player['marketValue'].replace(',', '').replace('€', ''),
            image=get_player_image(player),
        )
        players.append(player)

    return players


def get_player(team_id, name):
    json = requests.get(
        'http://api.football-data.org/v1/teams/' + str(team_id) + '/players',
        headers={'X-Auth-Token': 'bf0513ea0ba6457fb4ae6d380cca8365'}
    ).json()

    for player in json['players']:
        if player['name'].replace(' ', '') == name:
            for key, value in Player.POSITION:
                if value == player['position']:
                    # TODO Validity check
                    pass

            player, created = Player.objects.get_or_create(
                name=player['name'],
                position=player['position'],
                jersey_number=player['jerseyNumber'],
                date_of_birth=player['dateOfBirth'],
                nationality=player['nationality'],
                contract_until=player['contractUntil'],
                market_value=player['marketValue'].replace(',', '').replace('€', ''),
                image=get_player_image(player),
            )

            return player
    return None
