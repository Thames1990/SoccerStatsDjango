import logging
import requests
import time

logger = logging.getLogger(__name__)


def timing(f):
    """
    Decorator to time functions in seconds.
    :param f: Function
    :return: Decorator
    """

    def wrap(*args):
        start_time = time.time()
        ret = f(*args)
        end_time = time.time()
        logger.info('%s function took %2.2f seconds' % (f.__name__, end_time - start_time))
        return ret

    return wrap


def rate_limited(max_per_second):
    """
    Decorator to limit functions calls per second.
    :param max_per_second: Maximum of function calls per second
    :return: Decorator
    """
    min_interval = 1.0 / float(max_per_second)

    def decorate(func):
        last_time_called = [0.0]

        def rate_limited_function(*args, **kargs):
            elapsed = time.clock() - last_time_called[0]
            left_to_wait = min_interval - elapsed
            if left_to_wait > 0:
                time.sleep(left_to_wait)
            ret = func(*args, **kargs)
            last_time_called[0] = time.clock()
            return ret

        return rate_limited_function

    return decorate


def get_wikipedia_image(query):
    """
    Gets the Wikipedia page image for a site with name *query*
    :param query: Search term
    :return: URL to the Wikimedia page image if it exists; None otherwise
    """
    from json.decoder import JSONDecodeError

    response = requests.get(
        url='https://en.wikipedia.org/w/api.php',
        params={
            'action': 'query',
            'format': 'json',
            'generator': 'search',
            'gsrsearch': query,
            'gsrlimit': 1,
            'prop': 'pageimages',
            'piprop': 'thumbnail',
            'pilimit': 'max',
            'pithumbsize': 400
        }
    )
    try:
        json = response.json()
        try:
            return list(json['query']['pages'].values())[0]['thumbnail']['source']
        except KeyError:
            # TODO Implement different image provider
            return None
    except JSONDecodeError:
        logger.error('Couldn\'t get Wikipedia image for query: ' + query)
        logger.error('Response: ' + response.text)
        return None


def create_index_content():
    from competition.models import Competition
    from fixture.models import Fixture
    from player.models import Player
    from team.models import Team

    from player.utils import get_market_value_average
    from table.utils import get_tables_current_matchday, get_goals_record, get_goals_against_record, get_points_record
    from team.utils import get_squad_market_value_average

    competitions = Competition.objects.only('id', 'caption', 'current_matchday', 'last_updated')
    competition_count = len(competitions)

    last_five_finished_fixtures = Fixture.objects.filter(status='FINISHED').order_by('-date')[:5]
    fixture_count = Fixture.objects.count()

    best_three_players = Player.objects.filter(market_value__isnull=False).order_by('-market_value')[:3]
    player_count = Player.objects.count()
    market_value_average = get_market_value_average()

    tables_current_matchday = get_tables_current_matchday()
    table_count = len(tables_current_matchday)
    goals_record = get_goals_record()
    goals_against_record = get_goals_against_record()
    points_record = get_points_record()

    best_ten_teams = Team.objects.filter(squad_market_value__isnull=False).order_by('-squad_market_value')[:10]
    team_count = Team.objects.count()
    squad_market_value_average = get_squad_market_value_average()

    return {
        'competitions': competitions,
        'competition_count': competition_count,
        'last_five_finished_fixtures': last_five_finished_fixtures,
        'fixture_count': fixture_count,
        'best_three_players': best_three_players,
        'player_count': player_count,
        'market_value_average': market_value_average,
        'tables_current_matchday': tables_current_matchday,
        'table_count': table_count,
        'goals_record': goals_record,
        'goals_against_record': goals_against_record,
        'points_record': points_record,
        'best_ten_teams': best_ten_teams,
        'team_count': team_count,
        'squad_market_value_average': squad_market_value_average,
    }


@timing
def create_database():
    """
    Creates whole database.
    :return: Dictionary of created database
    """
    from competition.utils import create_competitions
    from fixture.utils import create_fixtures
    from player.utils import create_players
    from table.utils import create_tables
    from team.utils import create_teams

    logger.info('Creating database...')

    competitions = create_competitions()
    teams = create_teams()
    time.sleep(60)
    fixtures = create_fixtures()
    time.sleep(60)
    players = create_players()
    time.sleep(60)
    tables = create_tables()

    logger.info('Created database...')

    return {
        'competitions': competitions,
        'fixtures': fixtures,
        'players': players,
        'tables': tables,
        'teams': teams,
    }


@timing
def update_database():
    """
    Updates whole database.
    :return: Dictionary of updated database
    """
    from competition.utils import update_competitions
    from fixture.utils import update_fixtures
    from player.utils import update_players
    from table.utils import update_tables
    from team.utils import update_teams

    logger.info('Updating database...')

    competitions = update_competitions()
    teams = update_teams()
    time.sleep(60)
    fixtures = update_fixtures()
    time.sleep(60)
    players = update_players()
    time.sleep(60)
    tables = update_tables()

    logger.info('Updated database...')

    return {
        'competitions': competitions,
        'fixtures': fixtures,
        'players': players,
        'tables': tables,
        'teams': teams,
    }
