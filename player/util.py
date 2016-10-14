import requests
import wikipedia
import logging

from moneyed import Money
from player.models import Player


def get_players(team_id):
    json = requests.get(
        'http://api.football-data.org/v1/teams/' + str(team_id) + '/players',
        headers={'X-Auth-Token': 'bf0513ea0ba6457fb4ae6d380cca8365'}
    ).json()

    players = []

    # TODO Improve image search
    wikipedia.set_lang('de')
    for player in json['players']:
        image = None
        try:
            main_image = wikipedia.page(player['name']).images[0]
            if main_image.lower().endswith('.jpg') or main_image.lower().endswith('.svg'):
                image = main_image
            else:
                logging.error(main_image)
        except wikipedia.exceptions.DisambiguationError as disambiguation:
            for option in disambiguation.options:
                logging.error(option)
                # image = wikipedia.page(disambiguation.options[0]).images[0]
        except wikipedia.exceptions.PageError as page:
            logging.error(page)
            continue

        players.append(
            Player.objects.get_or_create(
                name=player['name'],
                position=player['position'],
                jersey_number=player['jerseyNumber'],
                date_of_birth=player['dateOfBirth'],
                nationality=player['nationality'],
                contract_until=player['contractUntil'],
                market_value=Money(player['marketValue'].replace(',', '').replace('€', ''), currency='EUR'),
                image=image,
            )[0]
        )

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

            image = wikipedia.page(name).images[0]

            return Player.objects.get_or_create(
                name=player['name'],
                position=player['position'],
                jersey_number=player['jerseyNumber'],
                date_of_birth=player['dateOfBirth'],
                nationality=player['nationality'],
                contract_until=player['contractUntil'],
                market_value=Money(player['marketValue'].replace(',', '').replace('€', ''), currency='EUR'),
                image=image,
            )[0]

    return None
