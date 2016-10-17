from django.shortcuts import render

from .util import get_or_create_team, get_or_create_competition_teams


def team_view(request, team_id):
    return render(request, 'team/team.html', {'team': get_or_create_team(team_id)})


def teams_view(request, competition_id):
    return render(request, 'team/teams.html', {'teams': get_or_create_competition_teams(competition_id)})
