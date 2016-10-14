from django.shortcuts import render
import logging

from .util import get_player


def index_view(request, team_id, player_name):
    player = get_player(team_id, player_name)
    return render(request, 'player/index.html', {
        'player': player,
    })
