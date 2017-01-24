import logging
import re
import requests

from django.utils.dateparse import parse_date

from SoccerStats.utils import timing, get_wikipedia_image, rate_limited
from competition.utils import fetch_competitions

from player.models import Player
from team.models import Team
from team.utils import fetch_teams

logger = logging.getLogger(__name__)


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


@timing
def create_players():
    """
    Creates all players.
    :return: List of created players
    """
    logger.info('Creating players...')

    player_objects = []

    for team in Team.objects.all():
        players = fetch_players(team.id)
        if players:
            for player in players:
                player_objects.append(
                    Player(
                        team=team,
                        name=player['name'],
                        position=dict(Player.POSITION)[player['position']],
                        jersey_number=player['jerseyNumber'] or None,
                        date_of_birth=parse_date(player['dateOfBirth']) if player['dateOfBirth'] else None,
                        nationality=dict(Player.NATIONALITY)[player['nationality']],
                        contract_until=parse_date(player['contractUntil']) if player['contractUntil'] else None,
                        market_value=re.sub('[^0-9]', '', player['marketValue']) if player['marketValue'] else None,
                        image=get_wikipedia_image(player['name']),
                    )
                )

    created_players = Player.objects.bulk_create(player_objects)
    logger.info('Created ' + str(len(created_players)) + ' players')
    return created_players


@timing
def update_players():
    """
    Updates all players. Updates the fields, if a matching player already exists; creates a new player otherwise.
    :return: List of updated players
    """
    logger.info('Updating players...')

    updated_players = []
    created_players = 0

    for team in Team.objects.all():
        players = fetch_players(team.id)
        if players:
            for player in players:
                player_object, created = Player.objects.update_or_create(
                    name=player['name'],
                    date_of_birth=parse_date(player['dateOfBirth']) if player['dateOfBirth'] else None,
                    nationality=dict(Player.NATIONALITY)[player['nationality']],
                    defaults={
                        'team': team,
                        'name': player['name'],
                        'position': dict(Player.POSITION)[player['position']],
                        'jersey_number': player['jerseyNumber'] or None,
                        'date_of_birth': parse_date(player['dateOfBirth']) if player['dateOfBirth'] else None,
                        'nationality': dict(Player.NATIONALITY)[player['nationality']],
                        'contract_until': parse_date(player['contractUntil']) if player['contractUntil'] else None,
                        'market_value': re.sub('[^0-9]', '', player['marketValue']) if player['marketValue'] else None,
                        'image': get_wikipedia_image(player['name']),
                    }
                )

                if created:
                    created_players += 1
                else:
                    updated_players.append(player_object)

    logger.info('Updated ' + str(len(updated_players)) + ' players, created ' + str(created_players))
    return updated_players


def get_positions():
    """
    Generate a set of all player positions available from the REST database.
    :return: Pretty printed set of all player positions available from the REST database
    """
    from pprint import pprint

    positions = set()
    for competition in fetch_competitions():
        for team in fetch_teams(competition['id']):
            players = fetch_players(re.sub('[^0-9]', '', team['_links']['self']['href'])[1:])
            if players:
                for player in players:
                    positions.add(player['position'])
    return pprint(positions)


def get_nationalities():
    """
    Generate a set of all player nationalities available from the REST database.
    :return: Pretty printed set of all player nationalities available from the REST database
    """
    from pprint import pprint

    nationalities = set()
    for competition in fetch_competitions():
        for team in fetch_teams(competition['id']):
            players = fetch_players(re.sub('[^0-9]', '', team['_links']['self']['href'])[1:])
            if players:
                for player in players:
                    nationalities.add(player['nationality'])
    return pprint(nationalities)
