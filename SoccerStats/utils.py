import logging
import time

import requests

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
    json = requests.get(
        url='http://en.wikipedia.org/w/api.php',
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
        }).json()
    try:
        return list(json['query']['pages'].values())[0]['thumbnail']['source']
    except KeyError:
        # TODO Implement different image provider
        return None


def create_database():
    """
    Creates whole database.
    :return:
    """
    from competition.utils import create_competitions
    from fixture.utils import create_fixtures
    from player.utils import create_players
    from table.utils import create_tables
    from team.utils import create_teams

    create_competitions()
    create_teams()
    create_players()
    create_tables()
    create_fixtures()


def update_database():
    """
    Updates whole database.
    :return:
    """
    from competition.utils import update_competitions
    from fixture.utils import update_fixtures
    from player.utils import update_players
    from table.utils import update_tables
    from team.utils import update_teams

    update_competitions()
    update_teams()
    update_players()
    update_tables()
    update_fixtures()
