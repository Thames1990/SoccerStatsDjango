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


@timing
def create_database():
    """
    Creates whole database.
    :return: Dictionary of created database
    """
    from competition.utils import create_competitions
    from fixture.utils import create_fixtures
    from player.utils import create_players, update_image_links
    from table.utils import create_tables
    from team.utils import create_teams, update_crest_url_links

    logger.info('Creating database...')

    competitions = create_competitions()
    teams = create_teams()
    update_crest_url_links()
    fixtures = create_fixtures()
    time.sleep(60)
    players = create_players()
    update_image_links()
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
    from player.utils import update_players, update_image_links
    from table.utils import update_tables
    from team.utils import update_teams, update_crest_url_links

    logger.info('Updating database...')

    competitions = update_competitions()
    teams = update_teams()
    update_crest_url_links()
    fixtures = update_fixtures()
    time.sleep(60)
    players = update_players()
    update_image_links()
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
