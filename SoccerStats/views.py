from django.shortcuts import render


def index(request):
    from competition.models import Competition
    from fixture.models import Fixture
    from player.models import Player
    from team.models import Team

    from player.utils import get_market_value_average
    from table.utils import get_tables_current_matchday, get_records
    from team.utils import get_squad_market_value_average

    last_five_finished_fixtures = Fixture.objects.filter(status='Beendet').order_by('-date')[:5]
    fixture_count = Fixture.objects.count()

    best_three_players = Player.objects.filter(market_value__isnull=False).order_by('-market_value')[:3]
    player_count = Player.objects.count()
    market_value_average = get_market_value_average()

    tables_current_matchday = get_tables_current_matchday()
    table_count = len(tables_current_matchday)
    records = get_records()

    best_ten_teams = Team.objects.filter(squad_market_value__isnull=False).order_by('-squad_market_value')[:10]
    team_count = Team.objects.count()
    squad_market_value_average = get_squad_market_value_average()

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
