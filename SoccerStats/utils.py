import logging
import time

logger = logging.getLogger(__name__)


def timing(f):
    """
    Decorator to time functions in milliseconds.
    :param f: Function
    :return: Decorator
    """

    def wrap(*args):
        start_time = time.time()
        ret = f(*args)
        end_time = time.time()
        logger.info('%s function took %0.3f ms' % (f.__name__, (end_time - start_time) * 1000.0))
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


def create_database():
    """
    Create whole database.
    :return:
    """
    from competition.utils import create_competitions
    from team.utils import create_teams
    from player.utils import create_players
    from fixture.utils import create_fixtures
    from table.utils import create_tables

    create_competitions()
    create_teams()
    create_players()
    create_fixtures()
    create_tables()


def update_database():
    """
    Update whole database.
    :return:
    """
    from competition.utils import update_competitions
    from team.utils import update_teams
    from player.utils import update_players
    from fixture.utils import update_fixtures
    from table.utils import update_tables

    update_competitions()
    update_teams()
    update_players()
    update_fixtures()
    update_tables()
