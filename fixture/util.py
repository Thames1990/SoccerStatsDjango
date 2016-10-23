def fetch_fixtures(competition_id):
    import requests

    return requests.get(
        'http://api.football-data.org/v1/competitions/' + str(competition_id) + '/fixtures',
        headers={'X-Auth-Token': 'bf0513ea0ba6457fb4ae6d380cca8365'}
    ).json()['fixtures']


def get_fixtures(competition_id):
    for fixture in fetch_fixtures(competition_id):
        from fixture.models import Fixture
        from competition.models import Competition
        from team.models import Team
        import re

        fxt = Fixture.objects.get_or_create(
            competition=Competition.objects.get(id=re.sub('[^0-9]', '', fixture['_links']['competition']['href'])[1:]),
            home_team=Team.objects.get(id=re.sub('[^0-9]', '', fixture['_links']['homeTeam']['href'])[1:]),
            away_team=Team.objects.get(id=re.sub('[^0-9]', '', fixture['_links']['awayTeam']['href'])[1:]),
            date=fixture['date'],
            status=fixture['status'],
            matchday=int(fixture['matchday']),
            home_team_name=fixture['homeTeamName'],
            away_team_name=fixture['awayTeamName'],
        )[0]

        from fixture.models import Result

        result = Result.objects.get_or_create(
            fixture=fxt,
            goals_home_team=int(fixture['result']['goalsHomeTeam']) if fixture['result']['goalsHomeTeam'] else None,
            goals_away_team=int(fixture['result']['goalsAwayTeam']) if fixture['result']['goalsAwayTeam'] else None,
        )[0]

        if 'halfTime' in fixture['result']:
            from fixture.models import HalfTime

            HalfTime.objects.get_or_create(
                result=result,
                goals_home_team=int(fixture['result']['halfTime']['goalsHomeTeam']),
                goals_away_team=int(fixture['result']['halfTime']['goalsAwayTeam']),
            )

        if 'extraTime' in fixture['result']:
            from fixture.models import ExtraTime

            ExtraTime.objects.get_or_create(
                result=result,
                goals_home_team=int(fixture['result']['extraTime']['goalsHomeTeam']),
                goals_away_team=int(fixture['result']['extraTime']['goalsAwayTeam']),
            )

        if 'penaltyShootout' in fixture['result']:
            from fixture.models import PenaltyShootout

            PenaltyShootout.objects.get_or_create(
                result=result,
                goals_home_team=int(fixture['result']['penaltyShootout']['goalsHomeTeam']),
                goals_away_team=int(fixture['result']['penaltyShootout']['goalsAwayTeam']),
            )

        if fixture['odds']:
            from fixture.models import Odds

            Odds.objects.get_or_create(
                fixture=fxt,
                home_win=fixture['odds']['homeWin'],
                draw=fixture['odds']['draw'],
                away_win=fixture['odds']['awayWin'],
            )


def get_all_fixtures():
    from competition.util import fetch_competitions

    for competition in fetch_competitions():
        get_fixtures(competition['id'])
