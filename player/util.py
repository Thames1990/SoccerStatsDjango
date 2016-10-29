import requests


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
    try:
        return requests.get(
            url='http://api.football-data.org/v1/teams/' + str(team_id) + '/players',
            headers={'X-Auth-Token': 'bf0513ea0ba6457fb4ae6d380cca8365'}
        ).json()['players']
    except KeyError:
        # TODO Log teams without players
        # Return empty dictionary for iterable loop check
        return {}


def get_players(team_id):
    from player.models import Player

    for player in fetch_players(team_id):
        # Empty players indicate an empty player list
        if not player:
            break

        from team.models import Team
        import re

        Player.objects.get_or_create(
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


def get_all_players():
    from team.models import Team

    for team in Team.objects.all():
        get_players(team.id)
