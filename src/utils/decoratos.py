"""This module contains decorators that can be used to modify the behavior of functions."""
import time
from collections.abc import Callable
from typing import Any

from src.utils.logger import create_logger


def timeit(method: Callable[..., Any]) -> Callable[..., Any]:
    """A decorator that measures the execution time of a method.

    Useful when comparing execution times of different methods.

    Args:
        method (Callable[..., Any]): The method to be timed.

    Returns:
        Callable[..., Any]: The decorated function which will print the execution time when called.
    """
    log = create_logger("time")

    def timed(*args: Any, **kwargs: Any) -> Any:
        """The actual wrapper that calculates the execution time.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Any: The result of the method being timed.
        """
        ts = time.time()  # Start time
        result = method(*args, **kwargs)  # Execute the method
        te = time.time()  # End time
        log.debug(f"{method.__name__} - {(te - ts):.3f}s")
        return result

    return timed
