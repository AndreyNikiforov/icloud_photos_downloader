import typing
from abc import abstractmethod
from enum import Enum
from typing import Any, Callable, Mapping, NewType, Optional, Protocol, Tuple, TypeVar, Union

from foundation.core import (
    apply_reverse,
    compact2,
    compose,
    curry2,
    curry3,
    expand2,
    fst,
    pipe,
    pipe2,
    snd,
    uncurry2,
)
from foundation.core.optional import bind, lift3

_Key = NewType("_Key", str)
_Tout = TypeVar("_Tout", covariant=True)


class _MappedByKey(Protocol[_Tout]):
    @abstractmethod
    def get(self, name: _Key) -> Optional[_Tout]:
        raise NotImplementedError


# Json typed representation
_JsonObject = _MappedByKey["_JsonNode"]
_JsonValue = Union[str, int, float]
_JsonNode = Union[_JsonValue, _JsonObject]

_MasterRecordNode = NewType("_MasterRecordNode", Mapping[_Key, Any])

_FieldsNode = NewType("_FieldsNode", Mapping[_Key, Any])

_ResNode = NewType("_ResNode", Mapping[_Key, Any])
_ResValueNode = NewType("_ResValueNode", Mapping[_Key, Any])
_ResValueSize = NewType("_ResValueSize", int)
_ResValueURL = NewType("_ResValueURL", str)

_FileTypeNode = NewType("_FileTypeNode", Mapping[_Key, Any])
_FileType = NewType("_FileType", str)

_ResourceKey = NewType("_ResourceKey", _Key)
_FileTypeKey = NewType("_FileTypeKey", _Key)


class _VariantFieldName(Enum):
    ORIGINAL = (_ResourceKey(_Key("resOriginalRes")), _FileTypeKey(_Key("resOriginalFileType")))
    ALTERNATIVE = (
        _ResourceKey(_Key("resOriginalAltRes")),
        _FileTypeKey(_Key("resOriginalAltFileType")),
    )
    MEDIUM = (_ResourceKey(_Key("resJPEGMedRes")), _FileTypeKey(_Key("resJPEGMedFileType")))
    THUMB = (_ResourceKey(_Key("resJPEGThumbRes")), _FileTypeKey(_Key("resJPEGThumbFileType")))
    ADJUSTED = (_ResourceKey(_Key("resJPEGFullRes")), _FileTypeKey(_Key("resJPEGFullFileType")))
    LIVE_ORIGINAL = (
        _ResourceKey(_Key("resOriginalVidComplRes")),
        _FileTypeKey(
            _Key("resOriginalVidComplFileType"),
        ),
    )
    VIDEO_MEDIUM = (_ResourceKey(_Key("resVidMedRes")), _FileTypeKey(_Key("resVidMedFileType")))
    VIDEO_SMALL = (_ResourceKey(_Key("resVidSmallRes")), _FileTypeKey(_Key("resVidSmallFileType")))

    def __str__(self) -> str:
        return self.name


_FILEDS_NAME = _Key("fields")
_VALUE_FILED_NAME = _Key("value")
_SIZE_FILED_NAME = _Key("size")
_URL_FILED_NAME = _Key("downloadURL")


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


_Tin = TypeVar("_Tin")
_Tin2 = TypeVar("_Tin2")

# mypy for functions with type params is not working
# def _match(ty: Type[_Tin], input: Union[_Tin, _Tin2]) -> Optional[_Tin]:
#     """matching input by type and returns None if not
#     >>> _match(int, 5)
#     5
#     >>> _match(str, 5) == None
#     True
#     """
#     if isinstance(input, ty):
#         return input
#     return None


# _match_c = curry2(_match)


# hard coded implementations, becaause mypy for function with Type param does not work
def _match_jo(input: Union[_JsonObject, Any]) -> Optional[_JsonObject]:
    """match json object
    >>> _match_jo({"foo": "bar"})
    {'foo': 'bar'}
    >>> _match_jo(5) == None
    True
    """
    try:
        g = input.get
        if g:
            return input
    except BaseException:
        pass
    return None


def _match_jv(input: Union[_JsonValue, Any]) -> Optional[_JsonValue]:
    """match json object
    >>> _match_jv({"foo": "bar"}) == None
    True
    >>> _match_jv(5)
    5
    >>> _match_jv(6.1)
    6.1
    >>> _match_jv("abc")
    'abc'
    """
    if isinstance(input, (str, int, float)):
        return input
    return None


# end hard coded impl

_attr_jo: Callable[[_Key, _JsonObject], Optional[_JsonObject]] = pipe2(_attr, bind(_match_jo))
_attr_jv: Callable[[_Key, _JsonObject], Optional[_JsonValue]] = pipe2(_attr, bind(_match_jv))

_attr_jo_c = curry2(_attr_jo)
_attr_jv_c = curry2(_attr_jv)

# _attr_jo = pipe2(_attr_j, bind(_match(_JsonObject)))


def _enum_value(  # cannot make it generic
    enum: Enum,
) -> Any:
    """get value of enumeration member"""
    return enum.value


# typed version for _VariantFieldName
_field_key = typing.cast(
    Callable[[_VariantFieldName], Tuple[_ResourceKey, _FileTypeKey]], _enum_value
)


_attr_c = curry2(_attr)

_master_fields_node: Callable[[_MasterRecordNode], Optional[_FieldsNode]] = _attr_c(_FILEDS_NAME)
# assert _master_fields_node({"fields": "bar"}) == "bar"

# typed version of getting field key from enum
_res_field_name = pipe(_field_key, fst)
# assert _res_field_name(_VariantFieldName.ORIGINAL) == "resOriginalRes"

# extracting resource node out of fields node
_res_node: Callable[[_VariantFieldName], Callable[[_FieldsNode], Optional[_ResNode]]] = pipe(
    _res_field_name, _attr_c
)
# assert _res_node(_VariantFieldName.ORIGINAL)({"resOriginalRes": {"bar": "baz"}}) == {"bar": "baz"}

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
_file_type_field_name = pipe(_field_key, snd)
# assert _file_type_field_name(_VariantFieldName.ORIGINAL) == "resOriginalFileType"

_file_type_node: Callable[[_VariantFieldName], Callable[[_FieldsNode], Optional[_FileTypeNode]]] = (
    pipe(_file_type_field_name, _attr_c)
)

_file_type_value: Callable[[_FileTypeNode], Optional[_FileType]] = _attr_c(_VALUE_FILED_NAME)


# _VariantFieldName -> _FieldsNode -> Optional[_ResValueSize]
_size = pipe(
    apply_reverse(_res_node),
    pipe(
        bind(_res_value_node),
        bind(_res_value_size),
    ),
)

# _VariantFieldName -> _FieldsNode -> Optional[_ResValueURL]
_url = pipe(
    apply_reverse(_res_node),
    pipe(
        bind(_res_value_node),
        bind(_res_value_url),
    ),
)


def _file_type2(input: _VariantFieldName) -> Callable[[_FieldsNode], Optional[_FileType]]:
    def _intern(input2: _FieldsNode) -> Optional[_FileType]:
        return bind(_file_type_value)(_file_type_node(input)(input2))

    return _intern


# print(_file_type2(_VariantFieldName.ORIGINAL)({"resOriginalFileType": "abc"}))


# _VariantFieldName -> _FieldsNode -> Optional[_FileType]
# _file_type: Callable[[_VariantFieldName], Callable[[_FieldsNode], Optional[_FileType]]] = pipe(
_file_type = curry2(
    expand2(
        pipe(
            compact2(uncurry2(_file_type_node)),
            bind(_file_type_value),
        )
    )
)
print(_file_type(_VariantFieldName.ORIGINAL))
# print(_file_type(_VariantFieldName.ORIGINAL)(_FieldsNode({"resOriginalFileType": "abc"})))

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

_compose_c = curry2(compose)

_pipe_c = curry2(pipe)

_compose2x = _compose_c(_compose_c)(_compose_c)
# _assert_version = _compose2x(_build_entry_c)(_file_type)

# def _extract_size_and_url(
#     prefix: str,
#     fields: Dict[str, Any],
#     ) -> Tuple[int, str]:

#     res_name = f"{prefix}Res"
#     size = fields[res_name]['value']['size']
#     download_url = fields[res_name]['value']['downloadURL']
#     return (size, download_url)
