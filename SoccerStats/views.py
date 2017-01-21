from django.shortcuts import render


def index(request):
    from competition.models import Competition
    from fixture.models import Fixture
    from player.models import Player
    from team.models import Team
    from django.db.models import Avg, Sum, DecimalField

    from table.utils import get_tables_current_matchday, get_goals_record, get_goals_against_record, get_points_record
    from team.utils import get_squad_market_value_average

    tables_current_matchday = get_tables_current_matchday()

    return render(request, 'SoccerStats/index.html', {
        'competition': {
            'list': Competition.objects.only('id', 'caption', 'current_matchday'),
            'count': Competition.objects.count(),
        },
        'fixture': {
            'count': Fixture.objects.count(),
            'last_five': Fixture.objects.filter(status='FINISHED').order_by('-date')[:5],
            'result_avg': Fixture.objects.aggregate(
                goals_home_team=Avg(
                    'result__goals_home_team',
                    output_field=DecimalField(decimal_places=2),
                ),
                goals_away_team=Avg(
                    'result__goals_away_team',
                    output_field=DecimalField(decimal_places=2),
                ),
            )
        },
        'player': {
            'count': Player.objects.count(),
            'market_value': Player.objects.aggregate(
                avg=Avg(
                    'market_value',
                    output_field=DecimalField(decimal_places=2),
                ),
            ),
            'best_three': Player.objects.order_by('-market_value')[:3],
        },
        'table': {
            'list': tables_current_matchday,
            'count': len(list(tables_current_matchday)),
            'goals_record': get_goals_record(),
            'goals_against_record': get_goals_against_record(),
            'points_record': get_points_record(),
        },
        'team': {
            'count': Team.objects.count(),
            'squad_market_value': get_squad_market_value_average(),
            'best_ten': sorted(
                Team.objects.all(),
                key=lambda team: team.get_squad_market_value(),
                reverse=True
            )[:10],
        }
    })


def error403(request):
    return render(request, 'SoccerStats/403.html')


def error404(request):
    return render(request, 'SoccerStats/404.html')


def error500(request):
    return render(request, 'SoccerStats/500.html')
