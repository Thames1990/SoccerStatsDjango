from django.db import transaction
from django.shortcuts import render


def index(request):
    from competition.models import Competition
    from fixture.models import Fixture
    from player.models import Player
    from table.models import CupTable
    from table.models import LeagueTable
    from team.models import Team
    from django.db.models import Avg, Sum, DecimalField, Max, Min, F, Q

    return render(request, 'SoccerStats/index.html', {
        'competition': {
            'list': Competition.objects.only('id', 'caption', 'current_matchday'),
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
            # TODO Only get last matchday
            # CupTable.objects.values('competition').annotate(current_matchday=Max('matchday'))
            'list': CupTable.objects.raw('''
            SELECT cup_table1.id, cup_table1.league_caption, cup_table1.matchday
            FROM table_cuptable cup_table1, (
              SELECT league_caption, MAX(matchday) AS current_matchday
              FROM table_cuptable
              GROUP BY league_caption
            ) AS cup_table2
            WHERE cup_table1.league_caption = cup_table2.league_caption AND cup_table1.matchday = cup_table2.current_matchday
            '''),
            'count': CupTable.objects.count(),
            'group_standing': CupTable.objects.aggregate(
                goals_avg=Avg(
                    'group__groupstanding__goals',
                    output_field=DecimalField(decimal_places=2),
                ),
            ),
        },
        'league_table': {
            # TODO Only get last matchday
            # LeagueTable.objects.values('competition').annotate(current_matchday=Max('matchday'))
            'list': LeagueTable.objects.raw('''
            SELECT league_table1.id, league_table1.league_caption, league_table1.matchday
            FROM table_leaguetable league_table1, (
              SELECT league_caption, MAX(matchday) AS current_matchday
              FROM table_leaguetable
              GROUP BY league_caption
            ) AS league_table2
            WHERE league_table1.league_caption = league_table2.league_caption AND league_table1.matchday = league_table2.current_matchday
            '''),
            'count': LeagueTable.objects.count(),
            'standing': LeagueTable.objects.aggregate(
                goals_avg=Avg(
                    'standing__goals',
                    output_field=DecimalField(decimal_places=2),
                ),
            ),
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
