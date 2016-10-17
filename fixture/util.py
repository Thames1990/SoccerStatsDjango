import requests

from fixture.models import Fixture, Result, HalfTime, ExtraTime, PenaltyShootout, Odds


def get_or_create_fixtures(fixture_id):
    fixtures = []
    for fixture in requests.get('http://api.football-data.org/v1/competitions/' + str(fixture_id) + '/fixtures',
                                headers={'X-Auth-Token': 'bf0513ea0ba6457fb4ae6d380cca8365'}
                                ).json()['fixtures']:
        fxt = Fixture.objects.get_or_create(
            date=fixture['date'],
            status=fixture['status'],
            matchday=int(fixture['matchday']),
            home_team_name=fixture['homeTeamName'],
            away_team_name=fixture['awayTeamName'],
        )[0]

        result = Result.objects.get_or_create(
            fixture=fxt,
            goals_home_team=int(fixture['result']['goalsHomeTeam']) if fixture['result']['goalsHomeTeam'] else None,
            goals_away_team=int(fixture['result']['goalsAwayTeam']) if fixture['result']['goalsAwayTeam'] else None,
        )[0]

        if 'halfTime' in fixture['result']:
            HalfTime.objects.get_or_create(
                result=result,
                goals_home_team=int(fixture['result']['halfTime']['goalsHomeTeam']),
                goals_away_team=int(fixture['result']['halfTime']['goalsAwayTeam']),
            )

        if 'extraTime' in fixture['result']:
            ExtraTime.objects.get_or_create(
                result=result,
                goals_home_team=int(fixture['result']['extraTime']['goalsHomeTeam']),
                goals_away_team=int(fixture['result']['extraTime']['goalsAwayTeam']),
            )

        if 'penaltyShootout' in fixture['result']:
            PenaltyShootout.objects.get_or_create(
                result=result,
                goals_home_team=int(fixture['result']['penaltyShootout']['goalsHomeTeam']),
                goals_away_team=int(fixture['result']['penaltyShootout']['goalsAwayTeam']),
            )

        if fixture['odds']:
            Odds.objects.get_or_create(
                fixture=fxt,
                home_win=fixture['odds']['homeWin'],
                draw=fixture['odds']['draw'],
                away_win=fixture['odds']['awayWin'],
            )

        fixtures.append(fxt)

    return fixtures
