import time


def timing(f):
    """
    Decorator to time functions in milliseconds.
    :param f: Function
    :return: Function name and time measurement
    """

    def wrap(*args):
        start_time = time.time()
        ret = f(*args)
        end_time = time.time()
        print('%s function took %0.3f ms' % (f.__name__, (end_time - start_time) * 1000.0))
        return ret

    return wrap


def rate_limited(max_per_second):
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
    from competition.utils import create_competitions
    from fixture.utils import create_fixtures
    from player.utils import create_players
    from table.utils import create_all_tables
    from team.utils import create_teams

    create_competitions()
    create_teams()
    create_players()
    create_fixtures()
    create_all_tables()
