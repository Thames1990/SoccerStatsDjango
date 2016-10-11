from django.shortcuts import render

from .models import CupID, LeagueID, LeagueTable, CupTable
from .util import get_table, get_league_table_position_changes, get_cup_table_position_changes


def index_view(request, competition_id):
    try:
        competition_id = LeagueID(int(competition_id))
    except ValueError:
        competition_id = CupID(int(competition_id))
    table = get_table(competition_id, None)
    if isinstance(table, LeagueTable):
        return render(request, 'footballData/index.html', {
            'league_table': table,
            'league_table_position_changes': get_league_table_position_changes(table, competition_id),
        })
    elif isinstance(table, CupTable):
        return render(request, 'footballData/index.html', {
            'cup_table': table,
            'cup_table_position_changes': get_cup_table_position_changes(table, competition_id),
        })
    else:
        return NotImplemented
