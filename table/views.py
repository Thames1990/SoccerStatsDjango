from django.shortcuts import render

from competition.models import CupId, LeagueId

from .models import LeagueTable, CupTable
from .util import get_table, get_league_table_position_changes, get_cup_table_position_changes


def index_view(request, competition_id):
    try:
        competition_id = LeagueId(int(competition_id))
    except ValueError:
        competition_id = CupId(int(competition_id))
    table = get_table(competition_id, None)
    if isinstance(table, LeagueTable):
        return render(request, 'table/index.html', {
            'league_table': table,
            'league_table_position_changes': get_league_table_position_changes(table, competition_id),
        })
    elif isinstance(table, CupTable):
        return render(request, 'table/index.html', {
            'cup_table': table,
            'cup_table_position_changes': get_cup_table_position_changes(table, competition_id),
        })
    else:
        return NotImplemented
