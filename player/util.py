import requests

from moneyed import Money
from player.models import Player


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

            return Player.objects.get_or_create(
                name=player['name'],
                position=player['position'],
                jersey_number=player['jerseyNumber'],
                date_of_birth=player['dateOfBirth'],
                nationality=player['nationality'],
                contract_until=player['contractUntil'],
                market_value=Money(player['marketValue'].replace(',', '').replace('€', ''), currency='EUR'),
            )[0]

    return None
