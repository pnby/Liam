import functools
import inspect
from typing import Callable, Any

from bot import get_session


def singleton(cls: Callable):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


def inject_repository(repo_class: Callable[..., Any]) -> Callable[..., Any]:
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            session = await get_session()
            repo_instance = repo_class(session)
            sig = inspect.signature(func)
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()
            for param in sig.parameters.values():
                if param.annotation == repo_class:
                    bound_args.arguments[param.name] = repo_instance
            return await func(*bound_args.args, **bound_args.kwargs)

        return wrapper

    return decorator
