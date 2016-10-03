from django.shortcuts import get_object_or_404, render

from .models import LeagueTable


def index(request):
    league_tables = LeagueTable.objects.all()
    return render(request, 'footballData/index.html', {
        'league_tables': league_tables
    })


def detail(request, football_data_id):
    league_table = get_object_or_404(LeagueTable, pk=football_data_id)
    return render(request, 'footballData/detail.html', {
        'league_table': league_table
    })
