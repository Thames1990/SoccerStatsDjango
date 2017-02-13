from django.shortcuts import render
from django.views.decorators.cache import cache_page


# @cache_page(60 * 60)
def index(request):
    from django.db.models import Avg

    from competition.models import Competition
    from fixture.models import Fixture
    from player.models import Player
    from team.models import Team

    from table.utils import get_tables_current_matchday, get_records

    # TODO Optimize duplicated times query warnings

    fixtures = Fixture.objects.all()
    last_five_finished_fixtures = fixtures.filter(status='Beendet').order_by('-date')[:5]
    fixture_count = len(fixtures)

    players = Player.objects.all()
    players_with_market_value = players.filter(market_value__isnull=False)
    best_three_players = players_with_market_value.order_by('-market_value')[:3]
    market_value_average = players_with_market_value.aggregate(Avg('market_value'))['market_value__avg']
    player_count = len(players)

    tables_current_matchday = get_tables_current_matchday()
    records = get_records()
    table_count = len(tables_current_matchday)

    teams = Team.objects.all()
    teams_with_squad_market_value = teams.filter(squad_market_value__isnull=False)
    best_ten_teams = teams_with_squad_market_value.order_by('-squad_market_value')[:10]
    squad_market_value_average = teams_with_squad_market_value.aggregate(
        Avg('squad_market_value')
    )['squad_market_value__avg']
    team_count = len(teams)

    return render(request, 'SoccerStats/index.html', {
        'competitions': Competition.objects.all(),
        'last_five_finished_fixtures': last_five_finished_fixtures,
        'fixture_count': fixture_count,
        'best_three_players': best_three_players,
        'player_count': player_count,
        'market_value_average': market_value_average,
        'tables_current_matchday': tables_current_matchday,
        'table_count': table_count,
        'records': records,
        'best_ten_teams': best_ten_teams,
        'team_count': team_count,
        'squad_market_value_average': squad_market_value_average,
    })


def error403(request):
    return render(request, 'SoccerStats/403.html')


def error404(request):
    return render(request, 'SoccerStats/404.html')


def error500(request):
    return render(request, 'SoccerStats/500.html')
