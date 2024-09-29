import typing
from abc import abstractmethod
from enum import Enum
from typing import Any, Callable, Mapping, NewType, Optional, Protocol, TypeVar

from foundation.core import apply_reverse, curry2, curry3, pipe
from foundation.core.optional import bind, lift3

_Key = NewType("_Key", str)
_MasterRecordNode = NewType("_MasterRecordNode", Mapping[_Key, Any])

_FieldsNode = NewType("_FieldsNode", Mapping[_Key, Any])

_ResNode = NewType("_ResNode", Mapping[_Key, Any])
_ResValueNode = NewType("_ResValueNode", Mapping[_Key, Any])
_ResValueSize = NewType("_ResValueSize", int)
_ResValueURL = NewType("_ResValueURL", str)

_FileTypeNode = NewType("_FileTypeNode", Mapping[_Key, Any])
_FileType = NewType("_FileType", str)


class _ResourceFieldName(Enum):
    ORIGINAL = _Key("resOriginalRes")
    ALTERNATIVE = _Key("resOriginalAltRes")
    MEDIUM = _Key("resJPEGMedRes")
    THUMB = _Key("resJPEGThumbRes")
    ADJUSTED = _Key("resJPEGFullRes")
    LIVE_ORIGINAL = _Key("resOriginalVidComplRes")
    VIDEO_MEDIUM = _Key("resVidMedRes")
    VIDEO_SMALL = _Key("resVidSmallRes")

    def __str__(self) -> str:
        return self.name


class _FileTypeFieldName(Enum):
    ORIGINAL = _Key("resOriginalFileType")
    ALTERNATIVE = _Key("resOriginalAltFileType")
    MEDIUM = _Key("resJPEGMedFileType")
    THUMB = _Key("resJPEGThumbFileType")
    ADJUSTED = _Key("resJPEGFullFileType")
    LIVE_ORIGINAL = _Key("resOriginalVidComplFileType")
    VIDEO_MEDIUM = _Key("resVidMedFileType")
    VIDEO_SMALL = _Key("resVidSmallFileType")

    def __str__(self) -> str:
        return self.name


_FILEDS_NAME = _Key("fields")
_VALUE_FILED_NAME = _Key("value")
_SIZE_FILED_NAME = _Key("size")
_URL_FILED_NAME = _Key("downloadURL")

_Tout = TypeVar("_Tout", covariant=True)


class _MappedByKey(Protocol[_Tout]):
    @abstractmethod
    def get(self, name: _Key) -> Optional[_Tout]:
        raise NotImplementedError


def _attr(  # cannot make it generic
    key: _Key,
    mapped: _MappedByKey[Any],
) -> Optional[_Tout]:
    """Get item on a Mapped by Key

    >>> _attr(_Key("foo"), {"foo": "bar"}) == "bar"
    True
    >>> _attr(_Key("baz"), {"foo": "bar"}) == None
    True

    """
    return mapped.get(key)


def _enum_value(  # cannot make it generic
    enum: Enum,
) -> Any:
    """get value of enumeration member"""
    return enum.value


_attr_c = curry2(_attr)

_master_fields_node: Callable[[_MasterRecordNode], Optional[_FieldsNode]] = _attr_c(_FILEDS_NAME)
# assert _master_fields_node({"fields": "bar"}) == "bar"

# typed version of getting field key from enum
_res_field_name = typing.cast(Callable[[_ResourceFieldName], _Key], _enum_value)

# extracting resource node out of fields node
_res_node: Callable[[_ResourceFieldName], Callable[[_FieldsNode], Optional[_ResNode]]] = pipe(
    _res_field_name, _attr_c
)
# assert _res_node(_ResourceFieldName.ORIGINAL)({"resOriginalRes": {"bar": "baz"}}) == {"bar": "baz"}

# extracting resource value node out of resource node
_res_value_node: Callable[[_ResNode], Optional[_ResValueNode]] = _attr_c(_VALUE_FILED_NAME)
# assert _res_value_node({"value": {"bar": "baz"}}) == {"bar": "baz"}

# extracting resource value size out of resource value node
_res_value_size: Callable[[_ResValueNode], Optional[_ResValueSize]] = _attr_c(_SIZE_FILED_NAME)
# assert _res_value_size({"size": 123}) == 123


# extracting resource value size out of resource value node
_res_value_url: Callable[[_ResValueNode], Optional[_ResValueURL]] = _attr_c(_URL_FILED_NAME)
# assert _res_value_url({"downloadURL": "abc"}) == "abc"


# typed version of getting field key from enum
_file_type_field_name = typing.cast(Callable[[_FileTypeFieldName], _Key], _enum_value)

_file_type_node: Callable[
    [_FileTypeFieldName], Callable[[_FieldsNode], Optional[_FileTypeNode]]
] = pipe(_file_type_field_name, _attr_c)

_file_type_value: Callable[[_FileTypeNode], Optional[_FileType]] = _attr_c(_VALUE_FILED_NAME)


_size = pipe(
    apply_reverse(_res_node),
    pipe(
        bind(_res_value_node),
        bind(_res_value_size),
    ),
)

_url = pipe(
    apply_reverse(_res_node),
    pipe(
        bind(_res_value_node),
        bind(_res_value_url),
    ),
)

_file_type = pipe(
    apply_reverse(_file_type_node),
    bind(_file_type_value),
)

# _ft = uncurry2(uncurry2(_file_type))


class AssetVariant:
    def __init__(self, file_type: _FileType, size: _ResValueSize, url: _ResValueURL) -> None:
        self.size = size
        self.url = url
        self.file_type = file_type

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, AssetVariant):
            # don't attempt to compare against unrelated types
            return NotImplemented
        return (
            self.size == other.size and self.url == other.url and self.file_type == other.file_type
        )


def _build_entry(file_type: _FileType, size: _ResValueSize, url: _ResValueURL) -> AssetVariant:
    return AssetVariant(file_type, size, url)


_build_entry_l = lift3(_build_entry)
_build_entry_c = curry3(_build_entry_l)

# f4 :: a -> b -> c -> d
# f1 :: a -> b
# f2 :: a -> b
# f3 :: a -> b
# f5 :: a -> b
# (.) :: (b -> c) -> (a -> b) -> (a -> c)
# (.3) :: (b -> c -> d -> e) -> (a -> b) -> (a -> c) -> (a -> d) -> (a -> e)

# https://stackoverflow.com/a/5822395
# (->) a - Functor and (.) is fmap for it
# fmap . fmap :: (Functor f, Functor f1) => (a -> b) -> f (f1 a) -> f (f1 b)
# f is (->) c and f1 is (->) d
# (a -> b) -> (->) c ((->) d a) -> (->) c ((->) d b)
# (a -> b) -> (c -> d -> a) -> (c -> d -> b)
# same as (.) . (.) ::  (b -> c) -> (a -> a1 -> b) -> a -> a1 -> c

# fmap . fmap . fmap
# :: (Functor f, Functor g, Functor h) => (a -> b) -> f (g (h a)) -> f (g (h b))
# f is (->) c
# g is (->) d
# h is (->) e
# (a -> b) -> (c -> d -> e -> a) -> (c -> d -> e -> b)

# _fmap2x = compose(compose, compose)

# def _extract_size_and_url(
#     prefix: str,
#     fields: Dict[str, Any],
#     ) -> Tuple[int, str]:

#     res_name = f"{prefix}Res"
#     size = fields[res_name]['value']['size']
#     download_url = fields[res_name]['value']['downloadURL']
#     return (size, download_url)
