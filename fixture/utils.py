import re

from SoccerStats.utils import timing
from competition.models import Competition
from fixture.models import Fixture, Result, HalfTime, ExtraTime, PenaltyShootout, Odds
from team.models import Team


def fetch_fixtures(competition_id):
    """
    Fetches JSON representation of fixtures from football-data.org.
    :param competition_id: Id of a competition
    :return: JSON representation of all fixtures of the competition
    """
    import requests

    return requests.get(
        'http://api.football-data.org/v1/competitions/' + str(competition_id) + '/fixtures',
        headers={'X-Auth-Token': 'bf0513ea0ba6457fb4ae6d380cca8365'}
    ).json()['fixtures']


@timing
def create_fixtures():
    """
    Create all fixtures.
    :return: Created fixtures
    """
    from competition.utils import fetch_competitions

    fixtures = []
    results = []
    half_times = []
    extra_times = []
    penalty_shootouts = []
    odds = []

    for competition in fetch_competitions():
        for fixture in fetch_fixtures(competition['id']):
            fixture_object = Fixture(
                id=re.sub('[^0-9]', '', fixture['_links']['self']['href'])[1:],
                competition=Competition.objects.get(
                    id=re.sub('[^0-9]', '', fixture['_links']['competition']['href'])[1:]
                ),
                home_team=Team.objects.get(id=re.sub('[^0-9]', '', fixture['_links']['homeTeam']['href'])[1:]),
                away_team=Team.objects.get(id=re.sub('[^0-9]', '', fixture['_links']['awayTeam']['href'])[1:]),
                # TODO Think about date conversion
                date=fixture['date'],
                status=dict(Fixture.STATUS)[fixture['status']] if fixture['status'] else None,
                matchday=int(fixture['matchday']),
            )
            fixtures.append(fixture_object)

            result = Result(
                id=fixture_object.id,
                fixture=fixture_object,
                # TODO Fix Zero goals evaluates to null (issue #1)
                goals_home_team=int(fixture['result']['goalsHomeTeam']) if fixture['result'][
                    'goalsHomeTeam'] else None,
                goals_away_team=int(fixture['result']['goalsAwayTeam']) if fixture['result'][
                    'goalsAwayTeam'] else None,
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
                        fixture=fixture_object,
                        home_win=fixture['odds']['homeWin'],
                        draw=fixture['odds']['draw'],
                        away_win=fixture['odds']['awayWin'],
                    )
                )

    Fixture.objects.bulk_create(fixtures)
    Result.objects.bulk_create(results)
    HalfTime.objects.bulk_create(half_times)
    ExtraTime.objects.bulk_create(extra_times)
    PenaltyShootout.objects.bulk_create(penalty_shootouts)
    Odds.objects.bulk_create(odds)

# TODO Add update function
