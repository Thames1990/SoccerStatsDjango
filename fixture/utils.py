import logging
import re

from django.utils.dateparse import parse_datetime

from competition.models import Competition
from fixture.models import Fixture, Result, HalfTime, ExtraTime, PenaltyShootout, Odd
from team.models import Team

from SoccerStats.utils import timing, rate_limited

logger = logging.getLogger(__name__)


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
        date=parse_datetime(fixture['date']),
        status=dict(Fixture.STATUS)[fixture['status']] if fixture['status'] else None,
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
    """
    Creates all fixtures.
    :return: Created fixtures, half times, extra times, penalty shootouts and odds
    """
    fixtures = []
    half_times = []
    extra_times = []
    penalty_shootouts = []
    odds = []

    for competition in Competition.objects.all():
        for fixture in fetch_fixtures(competition.id):
            fixture_object = create_fixture(fixture)
            fixtures.append(fixture_object)

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

    created_half_times = HalfTime.objects.bulk_create(half_times)
    created_extra_times = ExtraTime.objects.bulk_create(extra_times)
    created_penalty_shootouts = PenaltyShootout.objects.bulk_create(penalty_shootouts)
    created_odds = Odd.objects.bulk_create(odds)
    logger.info(
        'Created ' + str(len(fixtures)) + ' fixtures, ' +
        str(len(created_half_times)) + ' half times, ' +
        str(len(created_extra_times)) + ' extra times, ' +
        str(len(created_penalty_shootouts)) + ' penalty shootouts and ' +
        str(len(created_odds)) + ' odds.'
    )
    return {
        'fixtures': fixtures,
        'created_half_times': created_half_times,
        'created_extra_times': created_extra_times,
        'created_penalty_shootouts': created_penalty_shootouts,
        'created_odds': created_odds,
    }


@timing
def update_fixtures():
    """Updates all fixtures."""
    # TODO Stuff
    updated_fixtures = []
    created_fixtures = 0
    updated_results = []
    created_results = 0
    updated_half_times = []
    created_half_times = 0
    updated_extra_times = []
    created_extra_times = 0
    updated_penalty_shootouts = []
    created_penalty_shootouts = 0
    updated_odds = []
    created_odds = 0

    for competition in Competition.objects.all():
        for fixture in fetch_fixtures(competition.id):
            fixture_object, created = Fixture.objects.update_or_create(
                id=re.sub('[^0-9]', '', fixture['_links']['self']['href'])[1:],
                defaults={
                    'id': re.sub('[^0-9]', '', fixture['_links']['self']['href'])[1:],
                    'competition': Competition.objects.get(
                        id=re.sub('[^0-9]', '', fixture['_links']['competition']['href'])[1:]),
                    'home_team': Team.objects.get(id=re.sub('[^0-9]', '', fixture['_links']['homeTeam']['href'])[1:]),
                    'away_team': Team.objects.get(id=re.sub('[^0-9]', '', fixture['_links']['awayTeam']['href'])[1:]),
                    'date': parse_datetime(fixture['date']),
                    'status': dict(Fixture.STATUS)[fixture['status']] if fixture['status'] else None,
                    'matchday': int(fixture['matchday']),
                }
            )

            if created:
                created_fixtures += 1
            else:
                updated_fixtures.append(fixture_object)

            result = fixture['result']
            if (result['goalsHomeTeam'] or result['goalsHomeTeam'] == 0) and \
                    (result['goalsAwayTeam'] or result['goalsAwayTeam'] == 0):
                result_object, created = Result.objects.update_or_create(
                    id=fixture_object.id,
                    defaults={
                        'fixture': fixture_object,
                        'goals_home_team': int(fixture['result']['goalsHomeTeam']),
                        'goals_away_team': int(fixture['result']['goalsAwayTeam']),
                    }
                )
                if created:
                    created_results += 1

                    if 'halfTime' in result:
                        half_time, created = HalfTime.objects.update_or_create(
                            result=result_object,
                            defaults={
                                'result': result,
                                'goals_home_team': int(fixture['result']['halfTime']['goalsHomeTeam']),
                                'goals_away_team': int(fixture['result']['halfTime']['goalsAwayTeam']),
                            }
                        )
                        if created:
                            created_half_times += 1
                        else:
                            updated_half_times.append(half_time)

                    if 'extraTime' in result:
                        extra_time, created = ExtraTime.objects.update_or_create(
                            result=result_object,
                            defaults={
                                'result': result,
                                'goals_home_team': int(fixture['result']['extraTime']['goalsHomeTeam']),
                                'goals_away_team': int(fixture['result']['extraTime']['goalsAwayTeam']),
                            }
                        )
                        if created:
                            created_extra_times += 1
                        else:
                            updated_extra_times.append(extra_time)

                    if 'penaltyShootout' in result:
                        penalty_shootout, created = PenaltyShootout.objects.update_or_create(
                            result=result_object,
                            defaults={
                                'result': result,
                                'goals_home_team': int(fixture['result']['penaltyShootout']['goalsHomeTeam']),
                                'goals_away_team': int(fixture['result']['penaltyShootout']['goalsAwayTeam']),
                            }
                        )
                        if created:
                            created_penalty_shootouts += 1
                        else:
                            updated_penalty_shootouts.append(penalty_shootout)
                else:
                    updated_results.append(result_object)
            if fixture['odds']:
                odd, created = Odd.objects.update_or_create(
                    fixture=fixture_object,
                    defaults={
                        'fixture': fixture_object,
                        'home_win': fixture['odds']['homeWin'],
                        'draw': fixture['odds']['draw'],
                        'away_win': fixture['odds']['awayWin'],
                    }
                )
                if created:
                    created_odds += 1
                else:
                    updated_odds.append(odd)
