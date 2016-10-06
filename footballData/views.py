from django.views import generic

from .models import LeagueTable, LeagueID
from .util import get_league_table


class IndexView(generic.ListView):
    template_name = 'footballData/index.html'
    context_object_name = 'league_table'

    def get_queryset(self):
        return get_league_table(LeagueID.PL)


class DetailView(generic.DetailView):
    model = LeagueTable
    context_object_name = 'league_table'
    template_name = 'footballData/detail.html'
