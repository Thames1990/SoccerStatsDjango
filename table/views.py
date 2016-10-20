from django.views.generic import DetailView, ListView

from .models import CupTable, LeagueTable


# TODO Add position/rank changes as extra_context

class CupTableDetailView(DetailView):
    model = CupTable
    context_object_name = 'cup_table'


class CupTableListView(ListView):
    model = CupTable
    context_object_name = 'cup_tables'


class LeagueTableDetailView(DetailView):
    model = LeagueTable
    context_object_name = 'league_table'


class LeagueTableListView(ListView):
    model = LeagueTable
    context_object_name = 'league_tables'
