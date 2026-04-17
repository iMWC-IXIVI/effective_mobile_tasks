import time
import logging

from functools import wraps

from typing import Callable, Any


def timer(func: Callable) -> Callable:
    @wraps(func)
    async def wrapper(*args, **kwargs) -> Any:
        start_time = time.perf_counter()
        result = await func(*args, **kwargs)
        end_time = time.perf_counter()

        logging.info(f'{func.__name__} выполнялась - {end_time - start_time:.2f} сек.')

        return result
    return wrapper
