from django.shortcuts import render

from .util import get_players, get_player


def players_view(request, team_id):
    players = get_players(team_id)
    return render(request, 'player/players.html', {'players': players})


def player_view(request, team_id, player_name):
    player = get_player(team_id, player_name)
    return render(request, 'player/player.html', {
        'player': player,
    })
