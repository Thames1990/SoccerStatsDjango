from django.db import transaction
from django.shortcuts import render


def index(request):
    from competition.models import Competition
    from fixture.models import Fixture
    from player.models import Player
    from table.models import CupTable
    from table.models import LeagueTable
    from team.models import Team
    from django.db.models import Avg, Sum, DecimalField

    cup_tables_current_matchday = CupTable.objects.raw('''
            SELECT cup_table1.id, cup_table1.league_caption, cup_table1.matchday
            FROM table_cuptable cup_table1, (
              SELECT league_caption, MAX(matchday) AS current_matchday
              FROM table_cuptable
              GROUP BY league_caption
            ) AS cup_table2
            WHERE cup_table1.league_caption = cup_table2.league_caption
            AND cup_table1.matchday = cup_table2.current_matchday
            ''')

    league_tables_current_matchday = LeagueTable.objects.raw('''
            SELECT league_table1.id, league_table1.league_caption, league_table1.matchday
            FROM table_leaguetable league_table1, (
              SELECT league_caption, MAX(matchday) AS current_matchday
              FROM table_leaguetable
              GROUP BY league_caption
            ) AS league_table2
            WHERE league_table1.league_caption = league_table2.league_caption
            AND league_table1.matchday = league_table2.current_matchday
            ''')

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
            'list': cup_tables_current_matchday,
            'count': len(list(cup_tables_current_matchday)),
            # TODO
            # 'group_standing_goals_avg': sum(groupstanding.goals for groupstanding in
            #                                 (group.groupstanding_set.all() for group in
            #                                  (cup_table.group_set.all() for cup_table in
            #                                   cup_tables_current_matchday))) / len(list(cup_tables_current_matchday)),
        },
        'league_table': {
            'list': league_tables_current_matchday,
            'count': len(list(league_tables_current_matchday)),
            # TODO
            # 'standing_goals_avg': sum(standing.goals for standing in
            #                           (league_table.standing_set.all() for league_table in
            #                            league_tables_current_matchday)) / len(list(league_tables_current_matchday)),
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
