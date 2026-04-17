import time
import logging

from functools import wraps

from typing import Callable, Any


def timer(func: Callable) -> Callable:
    """Измерение времени выполнения функции"""

    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()

        logging.info(f'{func.__name__} выполнилась - {end_time - start_time:.2f} сек.')

        return result
    return wrapper
