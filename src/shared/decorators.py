from contextlib import suppress
import functools
from sqlalchemy.exc import NoResultFound, InternalError


def no_result(is_list: bool = False):
    def wrapper(func):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            with suppress(NoResultFound, InternalError):
                return func(*args, **kwargs)
            if is_list:
                return []
            return None

        return wrapped

    return wrapper
