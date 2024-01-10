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
_FirstType = TypeVar('_FirstType')
_SecondType = TypeVar('_SecondType')
_ThirdType = TypeVar('_ThirdType')
_UpdatedType = TypeVar('_UpdatedType')

_AppendableType = TypeVar('_AppendableType', bound='AppendableN')

# Used in laws:
_NewType1 = TypeVar('_NewType1')
_NewType2 = TypeVar('_NewType2')

@final
class _LawSpec(LawSpecDef):
    """
    Semigroup laws.

    # https://en.wikibooks.org/wiki/Haskell/The_Functor_class#The_functor_laws
    """

    __slots__ = ()

    @law_definition
    def associative_law(
        appendable: 'AppendableN[_FirstType, _SecondType, _ThirdType]',
        first: Callable[[_FirstType], _NewType1],
        second: Callable[[_NewType1], _NewType2],
    ) -> None:
        """Mapping twice or mapping a composition is the same thing."""
        assert_equal(
            appendable.concat(first).concat(second),
            appendable.concat(compose(first, second)),
        )

class AppendableN(
    Generic[_FirstType, _SecondType, _ThirdType],
    Lawful['AppendableN[_FirstType, _SecondType, _ThirdType]'],
):
    """
    Allows to concatenate wrapped values in containers.

    Behaves like a semigroup.

    See also:
        - https://en.wikipedia.org/wiki/Semigroup

    """

    __slots__ = ()

    _laws: ClassVar[Sequence[Law]] = (
        Law3(_LawSpec.associative_law),
    )

    @abstractmethod  # noqa: WPS125
    def concat(
        self: _AppendableType,
        function: Callable[[_FirstType], _UpdatedType],
    ) -> KindN[_AppendableType, _UpdatedType, _SecondType, _ThirdType]:
        """Allows to concatenate containers."""

#: Type alias for kinds with one type argument.
Appendable1 = AppendableN[_FirstType, NoReturn, NoReturn]

#: Type alias for kinds with two type arguments.
Appendable2 = AppendableN[_FirstType, _SecondType, NoReturn]

#: Type alias for kinds with three type arguments.
Appendable3 = AppendableN[_FirstType, _SecondType, _ThirdType]