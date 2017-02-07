import asyncio
from functools import wraps


def async_test(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # pylint: disable=not-callable
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(func(*args, **kwargs))
        return result
    return wrapper
