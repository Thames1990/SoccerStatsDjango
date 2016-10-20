from django.shortcuts import get_object_or_404, render

from team.models import Team


def team_view(request, team_id):
    return render(request, 'team/team.html', {
        'team': get_object_or_404(Team, id=team_id)
    })
