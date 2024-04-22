from functools import wraps
from time import time, process_time


def timing(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time()
        ts_process = process_time()
        result = f(*args, **kw)
        return *result, {'clock_time': time() - ts, 'process_time': process_time() - ts_process}

    return wrap
