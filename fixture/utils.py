import re

from competition.models import Competition
from fixture.models import Fixture, Result, HalfTime, ExtraTime, PenaltyShootout, Odd
from team.models import Team

from SoccerStats.utils import timing, rate_limited


@rate_limited(0.8)
def fetch_fixtures(competition_id):
    """
    Fetches JSON representation of fixtures from football-data.org.
    :param competition_id: Id of a competition
    :return: JSON representation of all fixtures of the competition with id *competition_id*
    """
    import requests

    return requests.get(
        url='http://api.football-data.org/v1/competitions/' + str(competition_id) + '/fixtures',
        headers={'X-Auth-Token': 'bf0513ea0ba6457fb4ae6d380cca8365'}
    ).json()['fixtures']


def create_fixture(fixture):
    """
    Creates a Fixture object.
    :param fixture: JSON representation of a fixture
    :return: Fixture database object created from *fixture* JSON representation
    """
    return Fixture.objects.create(
        id=re.sub('[^0-9]', '', fixture['_links']['self']['href'])[1:],
        competition=Competition.objects.get(id=re.sub('[^0-9]', '', fixture['_links']['competition']['href'])[1:]),
        home_team=Team.objects.get(id=re.sub('[^0-9]', '', fixture['_links']['homeTeam']['href'])[1:]),
        away_team=Team.objects.get(id=re.sub('[^0-9]', '', fixture['_links']['awayTeam']['href'])[1:]),
        date=fixture['date'],
        status=fixture['status'] or None,
        matchday=int(fixture['matchday']),
    )


def create_result(fixture_object, fixture):
    """
    Creates a Result object.
    :param fixture_object: Fixture object already created from *fixture* JSON representation
    :param fixture: JSON representation of a result
    :return: Result database object created from *fixture* JSON representation
    """
    return Result.objects.create(
        fixture=fixture_object,
        goals_home_team=int(fixture['result']['goalsHomeTeam']),
        goals_away_team=int(fixture['result']['goalsAwayTeam']),
    )


def create_half_time(result, fixture):
    """
    Creates a HalfTime object.
    :param result: Result object
    :param fixture: JSON representation of a fixture
    :return: HalfTime object created from *result* and *fixture* JSON representation
    """
    return HalfTime(
        result=result,
        goals_home_team=int(fixture['result']['halfTime']['goalsHomeTeam']),
        goals_away_team=int(fixture['result']['halfTime']['goalsAwayTeam']),
    )


def create_extra_time(result, fixture):
    """
    Creates a ExtraTime object.
    :param result: Result object
    :param fixture: JSON representation of a fixture
    :return: ExtraTime object created from *result* and *fixture* JSON representation
    """
    return ExtraTime(
        result=result,
        goals_home_team=int(fixture['result']['extraTime']['goalsHomeTeam']),
        goals_away_team=int(fixture['result']['extraTime']['goalsAwayTeam']),
    )


def create_penalty_shootouts(result, fixture):
    """
    Creates a PenaltyShootout object.
    :param result: Result object
    :param fixture: JSON representation of a fixture
    :return: PenaltyShootout object created from *result* and *fixture* JSON representation
    """
    return PenaltyShootout(
        result=result,
        goals_home_team=int(fixture['result']['penaltyShootout']['goalsHomeTeam']),
        goals_away_team=int(fixture['result']['penaltyShootout']['goalsAwayTeam']),
    )


def create_odds(fixture_object, fixture):
    """
    Creates a Odds object.
    :param fixture_object: Fixture object already created from *fixture* JSON representation
    :param fixture: JSON representation of a result
    :return: Odds object created from *fixture* JSON representation
    """
    return Odd(
        fixture=fixture_object,
        home_win=fixture['odds']['homeWin'],
        draw=fixture['odds']['draw'],
        away_win=fixture['odds']['awayWin'],
    )


@timing
def create_fixtures():
    """Creates all fixtures."""
    half_times = []
    extra_times = []
    penalty_shootouts = []
    odds = []

    for competition in Competition.objects.all():
        for fixture in fetch_fixtures(competition.id):
            fixture_object = create_fixture(fixture)

            if (fixture['result']['goalsHomeTeam'] or fixture['result']['goalsHomeTeam'] == 0) and \
                    (fixture['result']['goalsAwayTeam'] or fixture['result']['goalsAwayTeam'] == 0):
                result = create_result(fixture_object, fixture)

            if 'halfTime' in fixture['result']:
                half_times.append(create_half_time(result, fixture))

            if 'extraTime' in fixture['result']:
                extra_times.append(create_extra_time(result, fixture))

            if 'penaltyShootout' in fixture['result']:
                penalty_shootouts.append(create_penalty_shootouts(result, fixture))

            if fixture['odds']:
                odds.append(create_odds(fixture_object, fixture))

    HalfTime.objects.bulk_create(half_times)
    ExtraTime.objects.bulk_create(extra_times)
    PenaltyShootout.objects.bulk_create(penalty_shootouts)
    Odd.objects.bulk_create(odds)


@timing
def update_fixtures():
    """Updates all fixtures."""
    for competition in Competition.objects.all():
        for fixture in fetch_fixtures(competition.id):
            fixture_object = Fixture.objects.get(id=re.sub('[^0-9]', '', fixture['_links']['self']['href'])[1:])
            fixture_object.date = fixture['date']
            fixture_object.status = fixture['status'] or None
            fixture_object.save()

            result = fixture['result']
            if (result['goalsHomeTeam'] or result['goalsHomeTeam'] == 0) and \
                    (result['goalsAwayTeam'] or result['goalsAwayTeam'] == 0):
                result_object, created = Result.objects.get_or_create(id=fixture_object.id)
                if created:
                    result_object.goals_home_team = int(result['goalsHomeTeam'])
                    result_object.goals_away_team = int(result['goalsAwayTeam'])
                    result_object.save()

                    if 'halfTime' in result:
                        half_time, created = HalfTime.objects.get_or_create(result=result_object)
                        if created:
                            half_time.goals_home_team = int(result['halfTime']['goalsHomeTeam'])
                            half_time.goals_away_team = int(result['halfTime']['goalsAwayTeam'])
                            half_time.save()

                    if 'extraTime' in result:
                        extra_time, created = ExtraTime.objects.get_or_create(result=result_object)
                        if created:
                            extra_time.goals_home_team = int(result['extraTime']['goalsHomeTeam'])
                            extra_time.goals_away_team = int(result['extraTime']['goalsAwayTeam'])
                            extra_time.save()

                    if 'penaltyShootout' in result:
                        penalty_shootout, created = PenaltyShootout.objects.get_or_create(result=result_object)
                        if created:
                            penalty_shootout.goals_home_team = int(result['penaltyShootout']['goalsHomeTeam'])
                            penalty_shootout.goals_away_team = int(result['penaltyShootout']['goalsAwayTeam'])
                            penalty_shootout.save()

            if fixture['odds']:
                odd, created = Odd.objects.get_or_create(fixture=fixture_object)
                if created:
                    odd.home_win = fixture['odds']['homeWin']
                    odd.draw = fixture['odds']['draw']
                    odd.away_win = fixture['odds']['awayWin']
                    odd.save()
