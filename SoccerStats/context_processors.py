def competitions(request):
    from competition.models import Competition
    return {'competition_tuples': Competition.objects.values('id', 'caption')}


def fixtures(request):
    from fixture.models import Fixture
    return {
        'fixture_tuples': Fixture.objects.filter(status='FINISHED').values(
            'id',
            'home_team__name',
            'away_team__name',
            'status',
        ).order_by('-date')[:5]
    }


def players(request):
    from player.models import Player
    return {'player_tuples': Player.objects.values('id', 'name')[:5]}


def tables(request):
    from table.utils import get_tables_current_matchday
    return {'table_tuples': get_tables_current_matchday()}


def teams(request):
    from team.models import Team
    return {'team_tuples': Team.objects.values('id', 'name')[:5]}
