from django.shortcuts import render

from .models import LeagueID, CupID, LeagueTable, CupTable
from .util import get_table, get_league_table_position_changes, get_cup_table_position_changes


def index_view(request):
    table = get_table(CupID.CL, None)
    if isinstance(table, LeagueTable):
        return render(request, 'footballData/index.html', {
            'league_table': table,
            'league_table_position_changes': get_league_table_position_changes(table),
        })
    elif isinstance(table, CupTable):
        return render(request, 'footballData/index.html', {
            'cup_table': table,
            'cup_table_position_changes': get_cup_table_position_changes(table),
        })
    else:
        return NotImplemented
