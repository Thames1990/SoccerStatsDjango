from django.shortcuts import render


def index(request):
    from competition.models import Competition
    from fixture.models import Fixture
    from player.models import Player
    from table.models import CupTable
    from table.models import LeagueTable
    from team.models import Team
    from django.db.models import Avg, Sum
    from django.db.models import DecimalField
    return render(request, 'SoccerStats/index.html', {
        'competition': {
            'list': Competition.objects.values('id', 'caption', 'current_matchday'),
            'count': Competition.objects.count(),
            'team': Competition.objects.aggregate(count=Sum('number_of_teams'))
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
        'cup_table': {
            'list': CupTable.objects.values('id', 'league_caption'),
            'count': CupTable.objects.count(),
            'group_standing': CupTable.objects.aggregate(
                goals_avg=Avg(
                    'group__groupstanding__goals',
                    output_field=DecimalField(decimal_places=2),
                ),
            )
        },
        'league_table': {
            'list': LeagueTable.objects.values('id', 'league_caption'),
            'count': LeagueTable.objects.count(),
            'standing': LeagueTable.objects.aggregate(
                goals_avg=Avg(
                    'standing__goals',
                    output_field=DecimalField(decimal_places=2),
                ),
            )
        },
        'team': {
            'count': Team.objects.count(),
            'squad_market_value': Team.objects.aggregate(
                avg=Avg(
                    'squad_market_value',
                    output_field=DecimalField(decimal_places=2),
                )
            ),
            'best_five': Team.objects.order_by('-squad_market_value')[:5]
        }
    })


def error403(request):
    return render(request, 'SoccerStats/403.html')


def error404(request):
    return render(request, 'SoccerStats/404.html')


def error500(request):
    return render(request, 'SoccerStats/500.html')
