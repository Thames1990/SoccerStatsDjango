from django.shortcuts import render

from .util import get_or_create_competitions


def competitions_view(request):
    return render(request, 'competition/competitions.html', {
        'competitions': get_or_create_competitions(None),
    })


def competition_view(request, competition_id):
    return render(request, 'competition/competition.html', {
        'competition': get_or_create_competitions(competition_id),
    })
