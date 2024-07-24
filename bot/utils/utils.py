import functools
import inspect
from dataclasses import dataclass
from typing import Callable, Any

from bot import get_session


def singleton(cls: Callable):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance

