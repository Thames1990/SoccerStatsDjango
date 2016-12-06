from django.views.generic import DetailView, ListView

from .models import CupTable, LeagueTable

from .utils import get_cup_table_rank_changes, get_league_table_position_changes


class CupTableDetailView(DetailView):
    model = CupTable
    context_object_name = 'cup_table'

    def get_context_data(self, **kwargs):
        context = super(CupTableDetailView, self).get_context_data(**kwargs)
        context['cup_table_position_changes'] = get_cup_table_rank_changes(self.object)
        return context


class CupTableListView(ListView):
    model = CupTable
    context_object_name = 'cup_tables'


class LeagueTableDetailView(DetailView):
    model = LeagueTable
    context_object_name = 'league_table'

    def get_context_data(self, **kwargs):
        context = super(LeagueTableDetailView, self).get_context_data(**kwargs)
        context['league_table_position_changes'] = get_league_table_position_changes(self.object)
        return context


class LeagueTableListView(ListView):
    model = LeagueTable
    context_object_name = 'league_tables'
