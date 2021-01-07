"""
    Different Operators
"""

from typing import Callable, Any, Optional, Iterable

def compose(*functions: Callable[[Any], Any]) -> Callable[[Any], Any]:
    """
        Function composition
        compose(a,b,c)(x) === c(b(a(x)))
    """
    def _compose(source):
        result = source
        for func in functions:
            result = func(result)
        return result
    return _compose

def default_if_none(default_value: Any) -> Callable[[Optional[Any]], Any]:
    """
        Returns default value if parameter is None
    """

    def _default_if_none(source):
        if source is None:
            return default_value
        return source

    return _default_if_none

def all_or_none() -> Callable[[Iterable], Optional[Iterable]]:
    """
        Returns default value if parameter is None
    """

    def _all_or_none(source):
        if all(map(lambda x: x is not None, source)):
            return source
        return None
    return _all_or_none
