from competition.models import Competition
from fixture.models import Fixture, Result, HalfTime, ExtraTime, PenaltyShootout, Odds
from team.models import Team


def fetch_fixtures(competition_id):
    import requests

    return requests.get(
        'http://api.football-data.org/v1/competitions/' + str(competition_id) + '/fixtures',
        headers={'X-Auth-Token': 'bf0513ea0ba6457fb4ae6d380cca8365'}
    ).json()['fixtures']


def get_competition_fixtures(competition_id):
    fixtures = []
    results = []
    half_times = []
    extra_times = []
    penalty_shootouts = []
    odds = []

    for fixture in fetch_fixtures(competition_id):
        import re

        fxt = Fixture(
            competition=Competition.objects.get(id=re.sub('[^0-9]', '', fixture['_links']['competition']['href'])[1:]),
            home_team=Team.objects.get(id=re.sub('[^0-9]', '', fixture['_links']['homeTeam']['href'])[1:]),
            away_team=Team.objects.get(id=re.sub('[^0-9]', '', fixture['_links']['awayTeam']['href'])[1:]),
            date=fixture['date'],
            status=fixture['status'],
            matchday=int(fixture['matchday']),
        )
        fixtures.append(fxt)

        result = Result(
            fixture=fxt,
            # TODO Fix Zero goals evaluates to null
            goals_home_team=int(fixture['result']['goalsHomeTeam']) if fixture['result']['goalsHomeTeam'] else None,
            goals_away_team=int(fixture['result']['goalsAwayTeam']) if fixture['result']['goalsAwayTeam'] else None,
        )
        results.append(result)

        if 'halfTime' in fixture['result']:
            half_times.append(
                HalfTime(
                    result=result,
                    goals_home_team=int(fixture['result']['halfTime']['goalsHomeTeam']),
                    goals_away_team=int(fixture['result']['halfTime']['goalsAwayTeam']),
                )
            )

        if 'extraTime' in fixture['result']:
            extra_times.append(
                ExtraTime(
                    result=result,
                    goals_home_team=int(fixture['result']['extraTime']['goalsHomeTeam']),
                    goals_away_team=int(fixture['result']['extraTime']['goalsAwayTeam']),
                )
            )

        if 'penaltyShootout' in fixture['result']:
            penalty_shootouts.append(
                PenaltyShootout(
                    result=result,
                    goals_home_team=int(fixture['result']['penaltyShootout']['goalsHomeTeam']),
                    goals_away_team=int(fixture['result']['penaltyShootout']['goalsAwayTeam']),
                )
            )

        if fixture['odds']:
            odds.append(
                Odds(
                    fixture=fxt,
                    home_win=fixture['odds']['homeWin'],
                    draw=fixture['odds']['draw'],
                    away_win=fixture['odds']['awayWin'],
                )
            )

    return {
        'fixtures': fixtures,
        'results': results,
        'half_times': half_times,
        'extra_times': extra_times,
        'penalty_shootouts': penalty_shootouts,
        'odds': odds,
    }


def create_all_fixtures():
    from competition.util import fetch_competitions

    fixtures = []
    results = []
    half_times = []
    extra_times = []
    penalty_shootouts = []
    odds = []

    for competition in fetch_competitions():
        competition_fixtures = get_competition_fixtures(competition['id'])

        fixtures.extend(competition_fixtures['fixtures'])
        results.extend(competition_fixtures['results'])
        half_times.extend(competition_fixtures['half_times'])
        extra_times.extend(competition_fixtures['extra_times'])
        penalty_shootouts.extend(competition_fixtures['penalty_shootouts'])
        odds.extend(competition_fixtures['odds'])

    Fixture.objects.bulk_create(fixtures)
    Result.objects.bulk_create(results)
    HalfTime.objects.bulk_create(half_times)
    ExtraTime.objects.bulk_create(extra_times)
    PenaltyShootout.objects.bulk_create(penalty_shootouts)
    Odds.objects.bulk_create(odds)
