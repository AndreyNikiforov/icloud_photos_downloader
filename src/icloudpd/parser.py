from curses.ascii import isalpha, isdigit
from typing import Callable, Generic, Iterable, Protocol, Sequence, Tuple, TypeVar, Union
import typing

class ParserError(Exception):
    pass

_Tin = TypeVar("_Tin", contravariant=True)
_Tout = TypeVar("_Tout", covariant=True)
_Terr = TypeVar("_Terr", covariant=True, bound=ParserError)

class Parser(Protocol, Generic[_Tin, _Tout, _Terr]):
    def __call__(self, __values: Sequence[_Tin]) -> Union[_Terr, Tuple[_Tout, Sequence[_Tin]]]: ...


class UnexpectedEOSError(ParserError):
    def __init__(self) -> None:
        super().__init__("Unexpected End Of Stream")

class MissingExpectedEOSFError(ParserError):
    def __init__(self) -> None:
        super().__init__("Missing Expected End Of Stream")

class NotMatchingError(ParserError):
    def __init__(self) -> None:
        super().__init__("No match")

def satisfy(_pred: Callable[[_Tin], bool]) -> Parser[_Tin, _Tin, _Terr]:
    def _internal(_values:Sequence[_Tin]) -> Union[_Terr, Tuple[_Tin, Sequence[_Tin]]]:
        if len(_values) == 0:
            return typing.cast(_Terr, UnexpectedEOSError())
        _head = _values[0]
        _tail = _values[1:]
        if _pred(_head):
            return (_head, _tail)
        return typing.cast(_Terr, NotMatchingError())
    return _internal

_Tout1 = TypeVar("_Tout1", covariant=True)
_Tout2 = TypeVar("_Tout2", covariant=True)

def combine(_p1: Parser[_Tin, _Tout1, _Terr], _p2: Parser[_Tin, _Tout2, _Terr]) -> Parser[_Tin, Tuple[_Tout1, _Tout2], _Terr]:
    def _internal(_values:Sequence[_Tin]) -> Union[_Terr, Tuple[Tuple[_Tout1, _Tout2], Sequence[_Tin]]]:
        _r1 = _p1(_values)
        if isinstance(_r1, ParserError):
            return typing.cast(_Terr, _r1)
        else:
            _r1_head, _r1_tail = _r1
            _r2 = _p2(_r1_tail)
            if isinstance(_r2, ParserError):
                return typing.cast(_Terr, _r2)
            else:
                _r2_head, _r2_tail = _r2
                return ((_r1_head, _r2_head), _r2_tail)
    return _internal

def empty() -> Parser[_Tin, None, _Terr]:
    def _internal(_values:Sequence[_Tin]) -> Union[_Terr, Tuple[None, Sequence[_Tin]]]:
        if len(_values) == 0:
            return (None, _values)
        return typing.cast(_Terr, MissingExpectedEOSFError())
    return _internal

def either(_p1: Parser[_Tin, _Tout1, _Terr], _p2: Parser[_Tin, _Tout2, _Terr]) -> Parser[_Tin, Union[_Tout1, _Tout2], _Terr]:
    def _internal(_values:Sequence[_Tin]) -> Union[_Terr, Tuple[Union[_Tout1, _Tout2], Sequence[_Tin]]]:
        _r1 = _p1(_values)
        if isinstance(_r1, ParserError):
            _r2 = _p2(_values)
            if isinstance(_r2, ParserError):
                return typing.cast(_Terr, _r2)
            else:
                return _r2
        else:
            return _r1
    return _internal

def map(_f: Callable[[_Tout1], _Tout2]) -> Callable[[Parser[_Tin, _Tout1, _Terr]], Parser[_Tin, _Tout2, _Terr]]:
    def _internal(_p: Parser[_Tin, _Tout1, _Terr]) -> Parser[_Tin, _Tout2, _Terr]:
        def _subinternal(_values:Sequence[_Tin]) -> Union[_Terr, Tuple[_Tout2, Sequence[_Tin]]]:
            _r1 = _p(_values)
            if isinstance(_r1, ParserError):
                return typing.cast(_Terr, _r1)
            else:
                _r1_head, _r1_tail = _r1
                return (_f(_r1_head), _r1_tail)
        return _subinternal
    return _internal

def char(_char: str) -> Parser[str, str, _Terr]:
    return satisfy(lambda _c: _c == _char)

print(combine(combine(satisfy(isdigit),satisfy(isalpha)), empty())("1a"))
print(either(satisfy(isdigit),empty())("1"))
print(either(satisfy(isdigit),empty())(""))
print(combine(either(combine(char("1"),char("a")), char("1")), empty())("1a"))
print(combine(either(combine(char("1"),char("a")), char("1")), empty())("1"))
print(
    combine(
        either(
            combine(
                char("1"),
                map(lambda _c: _c.upper())(char("a"))
                ), 
            char("1")
            ), 
        empty()
        )
    ("1a"))
