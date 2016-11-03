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
