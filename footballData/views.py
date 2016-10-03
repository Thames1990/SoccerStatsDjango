from django.views import generic

from .models import LeagueTable
from .util import get_league_table


class IndexView(generic.ListView):
    template_name = 'footballData/index.html'
    context_object_name = 'league_table'

    def get_queryset(self):
        return get_league_table('http://api.football-data.org/v1/competitions/426/leagueTable')


class DetailView(generic.DetailView):
    model = LeagueTable
    context_object_name = 'league_table'
    template_name = 'footballData/detail.html'
