from abc import abstractmethod
from typing import Callable, ClassVar, Generic, NoReturn, Sequence, TypeVar, final
from returns.functions import compose, identity
from returns.primitives.asserts import assert_equal
from returns.primitives.hkt import KindN
from returns.primitives.laws import (
    Law,
    Law1,
    Law3,
    Lawful,
    LawSpecDef,
    law_definition,
)

from returns_ext.interfaces.appendable import AppendableN
_FirstType = TypeVar('_FirstType')
_SecondType = TypeVar('_SecondType')
_ThirdType = TypeVar('_ThirdType')
_UpdatedType = TypeVar('_UpdatedType')

_MonoidType = TypeVar('_MonoidType', bound='MonoidN')

# Used in laws:
# _NewType1 = TypeVar('_NewType1')
# _NewType2 = TypeVar('_NewType2')

# @final
# class _LawSpec(LawSpecDef):
#     """
#     Semigroup laws.

#     # https://en.wikibooks.org/wiki/Haskell/The_Functor_class#The_functor_laws
#     """

#     __slots__ = ()


#     @law_definition
#     def identity_law(
#         monoid: 'MonoidN[_FirstType, _SecondType, _ThirdType]',
#     ) -> None:
#         """Mapping identity over a value must return the value unchanged."""
#         assert_equal(MonoidN::empty(), monoid)


class MonoidN(
    AppendableN[_FirstType, _SecondType, _ThirdType],
):
    """
    Allows to concatenate wrapped values in containers and have an identify value.

    See also:
        - https://en.wikipedia.org/wiki/Monoid

    """

    __slots__ = ()

    # _laws: ClassVar[Sequence[Law]] = (
    #     Law1(_LawSpec.identity_law),
    # )

    @classmethod
    @abstractmethod
    def empty(cls
    ) -> KindN[_MonoidType, _UpdatedType, _SecondType, _ThirdType]:
        """Allows to create empty container."""

#: Type alias for kinds with one type argument.
Monoid1 = MonoidN[_FirstType, NoReturn, NoReturn]

#: Type alias for kinds with two type arguments.
Monoid2 = MonoidN[_FirstType, _SecondType, NoReturn]

#: Type alias for kinds with three type arguments.
Monoid3 = MonoidN[_FirstType, _SecondType, _ThirdType]