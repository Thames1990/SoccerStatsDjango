from django.shortcuts import render


def index(request):
    from competition.models import Competition
    from fixture.models import Fixture
    from player.models import Player
    from team.models import Team
    from django.db.models import Avg, Sum, DecimalField

    from table.utils import get_tables_current_matchday

    tables_current_matchday = get_tables_current_matchday()

    return render(request, 'SoccerStats/index.html', {
        'competition': {
            'list': Competition.objects.only('id', 'caption', 'current_matchday'),
            'count': Competition.objects.count(),
            'team': Competition.objects.aggregate(count=Sum('number_of_teams')),
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
            'best_five': Player.objects.order_by('-market_value')[:5],
        },
        'table': {
            'list': tables_current_matchday,
            'count': len(list(tables_current_matchday)),
        },
        'team': {
            'count': Team.objects.count(),
            'squad_market_value': Team.objects.aggregate(
                avg=Avg(
                    'squad_market_value',
                    output_field=DecimalField(decimal_places=2),
                )
            ),
            'best_five': Team.objects.order_by('-squad_market_value')[:5],
        }
    })


def error403(request):
    return render(request, 'SoccerStats/403.html')


def error404(request):
    return render(request, 'SoccerStats/404.html')


def error500(request):
    return render(request, 'SoccerStats/500.html')
