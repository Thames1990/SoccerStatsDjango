import logging
import os
import re

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
        url='https://api.football-data.org/v1/competitions/' + str(competition_id) + '/fixtures',
        headers={'X-Auth-Token': os.environ['X_AUTH_TOKEN']}
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
        status=dict(Fixture.STATUS)[fixture['status']] if fixture['status'] else None,
        matchday=fixture['matchday'],
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
        goals_home_team=fixture['result']['goalsHomeTeam'],
        goals_away_team=fixture['result']['goalsAwayTeam'],
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
        goals_home_team=fixture['result']['halfTime']['goalsHomeTeam'],
        goals_away_team=fixture['result']['halfTime']['goalsAwayTeam'],
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
        goals_home_team=fixture['result']['extraTime']['goalsHomeTeam'],
        goals_away_team=fixture['result']['extraTime']['goalsAwayTeam'],
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
        goals_home_team=fixture['result']['penaltyShootout']['goalsHomeTeam'],
        goals_away_team=fixture['result']['penaltyShootout']['goalsAwayTeam'],
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
    :return: Dictionary of created fixtures, half times, extra times, penalty shootouts and odds
    """
    logger.info('Creating fixtures...')

    fixtures = []
    results = []
    half_times = []
    extra_times = []
    penalty_shootouts = []
    odds = []

    for competition in Competition.objects.all():
        for fixture in fetch_fixtures(competition.id):
            fixture_object = create_fixture(fixture)
            fixtures.append(fixture_object)

            if (
                        (fixture['result']['goalsHomeTeam'] or fixture['result']['goalsHomeTeam'] == 0) and
                        (fixture['result']['goalsAwayTeam'] or fixture['result']['goalsAwayTeam'] == 0)
            ):
                result = create_result(fixture_object, fixture)
                results.append(result)

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

    logger.info('Created ' + str(len(fixtures)) + ' fixtures')
    logger.info('Created ' + str(len(results)) + ' results')
    logger.info('Created ' + str(len(created_half_times)) + ' half times')
    logger.info('Created ' + str(len(created_extra_times)) + ' extra times')
    logger.info('Created ' + str(len(created_penalty_shootouts)) + ' penalty shootouts')
    logger.info('Created ' + str(len(created_odds)) + ' odds')

    return {
        'fixtures': fixtures,
        'results': results,
        'created_half_times': created_half_times,
        'created_extra_times': created_extra_times,
        'created_penalty_shootouts': created_penalty_shootouts,
        'created_odds': created_odds,
    }


def update_or_create_fixture(fixture):
    """
    Updates or creates a fixture.
    :param fixture: JSON representation of the fixture
    :return: Updated or created fixture and *True*, if the fixture was created; *False* otherwise
    """
    return Fixture.objects.update_or_create(
        id=re.sub('[^0-9]', '', fixture['_links']['self']['href'])[1:],
        defaults={
            'id': re.sub('[^0-9]', '', fixture['_links']['self']['href'])[1:],
            'competition': Competition.objects.get(
                id=re.sub('[^0-9]', '', fixture['_links']['competition']['href'])[1:]
            ),
            'home_team': Team.objects.get(id=re.sub('[^0-9]', '', fixture['_links']['homeTeam']['href'])[1:]),
            'away_team': Team.objects.get(id=re.sub('[^0-9]', '', fixture['_links']['awayTeam']['href'])[1:]),
            'date': fixture['date'],
            'status': dict(Fixture.STATUS)[fixture['status']] if fixture['status'] else None,
            'matchday': fixture['matchday'],
        }
    )


def update_or_create_result(fixture_object, fixture):
    """
    Updates or creates a result.
    :param fixture_object: Linked fixture
    :param fixture: JSON representation of the fixture
    :return: Updated or created result and *True*, if the result was created; *False* otherwise
    """
    return Result.objects.update_or_create(
        id=fixture_object.id,
        defaults={
            'fixture': fixture_object,
            'goals_home_team': fixture['result']['goalsHomeTeam'],
            'goals_away_team': fixture['result']['goalsAwayTeam'],
        }
    )


def update_or_create_half_time(result_object, fixture):
    """
    Updates or creates a half time.
    :param result_object: Linked result
    :param fixture: JSON represantation of the fixture
    :return: Updated or created half time and *True*, if the half time was created; *False* otherwise
    """
    return HalfTime.objects.update_or_create(
        result=result_object,
        defaults={
            'result': result_object,
            'goals_home_team': fixture['result']['halfTime']['goalsHomeTeam'],
            'goals_away_team': fixture['result']['halfTime']['goalsAwayTeam'],
        }
    )


def update_or_create_extra_time(result_object, fixture):
    """
    Updates or creates an extra time.
    :param result_object: Linked result
    :param fixture: JSON representation of the fixture
    :return: Updated or created extra time and *True*, if the extra was created; *False* otherwise
    """
    return ExtraTime.objects.update_or_create(
        result=result_object,
        defaults={
            'result': result_object,
            'goals_home_team': fixture['result']['extraTime']['goalsHomeTeam'],
            'goals_away_team': fixture['result']['extraTime']['goalsAwayTeam'],
        }
    )


def update_or_create_penalty_shootout(result_object, fixture):
    """
    Updates or creates a penalty shootout.
    :param result_object: Linked result
    :param fixture: JSON representation of the fixture
    :return: Updated or created penalty shootout and *True*, if the penalty shootout was created; *False* otherwise
    """
    return PenaltyShootout.objects.update_or_create(
        result=result_object,
        defaults={
            'result': result_object,
            'goals_home_team': fixture['result']['penaltyShootout']['goalsHomeTeam'],
            'goals_away_team': fixture['result']['penaltyShootout']['goalsAwayTeam'],
        }
    )


def update_or_create_odd(fixture_object, fixture):
    """
    Updates or creates an odd.
    :param fixture_object: Linked fixture
    :param fixture: JSON representation of the fixture
    :return: Updated or created odd and *True*, if the odd was created; *False* otherwise
    """
    return Odd.objects.update_or_create(
        fixture=fixture_object,
        defaults={
            'fixture': fixture_object,
            'home_win': fixture['odds']['homeWin'],
            'draw': fixture['odds']['draw'],
            'away_win': fixture['odds']['awayWin'],
        }
    )


@timing
def update_fixtures():
    """
    Updates all fixtures
    :return: Dictionary of updated fixtures, results, half times, extra times, penalty shootouts and odds
    """
    logger.info('Updating fixtures...')

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
            fixture_object, created = update_or_create_fixture(fixture=fixture)

            if created:
                created_fixtures += 1
            else:
                updated_fixtures.append(fixture_object)

            result = fixture['result']
            if (
                        (result['goalsHomeTeam'] or result['goalsHomeTeam'] == 0) and
                        (result['goalsAwayTeam'] or result['goalsAwayTeam'] == 0)
            ):
                result_object, created = update_or_create_result(fixture_object=fixture_object, fixture=fixture)
                if created:
                    created_results += 1

                    if 'halfTime' in result:
                        half_time, created = update_or_create_half_time(result_object=result_object, fixture=fixture)

                        if created:
                            created_half_times += 1
                        else:
                            updated_half_times.append(half_time)
                    if 'extraTime' in result:
                        extra_time, created = update_or_create_extra_time(result_object=result_object, fixture=fixture)

                        if created:
                            created_extra_times += 1
                        else:
                            updated_extra_times.append(extra_time)
                    if 'penaltyShootout' in result:
                        penalty_shootout, created = update_or_create_penalty_shootout(
                            result_object=result_object,
                            fixture=fixture
                        )

                        if created:
                            created_penalty_shootouts += 1
                        else:
                            updated_penalty_shootouts.append(penalty_shootout)
                else:
                    updated_results.append(result_object)
            if fixture['odds']:
                odd, created = update_or_create_odd(fixture_object=fixture_object, fixture=fixture)

                if created:
                    created_odds += 1
                else:
                    updated_odds.append(odd)

    logger.info(
        'Updated ' + str(len(updated_fixtures)) + ' fixtures, ' +
        'created ' + str(created_fixtures)
    )
    logger.info(
        'Updated ' + str(len(updated_results)) + ' results, ' +
        'created ' + str(created_results)
    )
    logger.info(
        'Updated ' + str(len(updated_half_times)) + ' half times, ' +
        'created ' + str(created_half_times)
    )
    logger.info(
        'Updated ' + str(len(updated_extra_times)) + ' extra times, ' +
        'created ' + str(created_extra_times)
    )
    logger.info(
        'Updated ' + str(len(updated_penalty_shootouts)) + ' penalty shootouts, ' +
        'created ' + str(created_penalty_shootouts)
    )
    logger.info(
        'Updated ' + str(len(updated_odds)) + ' odds, ' +
        'created ' + str(created_odds)
    )

    return {
        'updated_fixtures': updated_fixtures,
        'updated_results': updated_results,
        'updated_half_times': updated_half_times,
        'updated_extra_times': updated_extra_times,
        'updated_penalty_shootouts': updated_penalty_shootouts,
        'updated_odds': updated_odds,
    }
