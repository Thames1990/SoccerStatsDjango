from django.shortcuts import render


def players_view(request, team_id):
    from player.util import get_players
    return render(request, 'player/players.html', {
        'players': get_players(team_id),
        'team_id': team_id
    })


def player_view(request, team_id, player_name):
    from player.util import get_player
    return render(request, 'player/player.html', {'player': get_player(team_id, player_name)})
