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
            'count': Competition.objects.count(),
            'team': Competition.objects.aggregate(count=Sum('number_of_teams'))
        },
        # 'fixture': {
        #     'result_avg': Fixture.objects.aggregate(
        #         goals_home_team=Avg('result__goals_home_team'),
        #         goals_away_team=Avg('result__goals_away_team'),
        #     )
        # },
        'cup_table': {
            'group_standing': CupTable.objects.aggregate(
                goals_avg=Avg(
                    'group__groupstanding__goals',
                    output_field=DecimalField(decimal_places=2)
                ),
                goals_against_avg=Avg(
                    'group__groupstanding__goals_against',
                    output_field=DecimalField(decimal_places=2)
                ),
            )
        },
        'team': {
            'count': Team.objects.count(),
            'squad_market_value': Team.objects.aggregate(avg=Avg('squad_market_value')),
        }
    })


def error403(request):
    return render(request, 'SoccerStats/403.html')


def error404(request):
    return render(request, 'SoccerStats/404.html')


def error500(request):
    return render(request, 'SoccerStats/500.html')
