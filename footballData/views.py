from django.shortcuts import render

from .models import LeagueID
from .util import get_league_table, get_league_table_position_changes


def index_view(request):
    league_table = get_league_table(LeagueID.BL1, None)
    return render(request, 'footballData/index.html', {
        'league_table': league_table,
        'league_table_position_changes': get_league_table_position_changes(league_table),
    })
