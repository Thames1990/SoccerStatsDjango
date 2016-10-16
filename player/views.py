from django.shortcuts import render

from .util import get_players, get_player


def players_view(request, team_id):
    return render(request, 'player/players.html', {
        'players': get_players(team_id),
        'team_id': team_id
    })


def player_view(request, team_id, player_name):
    return render(request, 'player/player.html', {'player': get_player(team_id, player_name)})
