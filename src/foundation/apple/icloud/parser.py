import typing
from enum import Enum
from typing import Any, Callable, Dict, NewType, Optional

from foundation.core import apply_reverse, curry3, pipe
from foundation.core.optional import bind, lift3

_MasterRecordNode = NewType("_MasterRecordNode", Dict[str, Any])

_FieldsNode = NewType("_FieldsNode", Dict[str, Any])

_ResNode = NewType("_ResNode", Dict[str, Any])
_ResValueNode = NewType("_ResValueNode", Dict[str, Any])
_ResValueSize = NewType("_ResValueSize", int)
_ResValueURL = NewType("_ResValueURL", str)

_FileTypeNode = NewType("_FileTypeNode", Dict[str, Any])
_FileType = NewType("_FileType", str)


class _ResourceFieldName(Enum):
    ORIGINAL = "resOriginalRes"
    ALTERNATIVE = "resOriginalAltRes"
    MEDIUM = "resJPEGMedRes"
    THUMB = "resJPEGThumbRes"
    ADJUSTED = "resJPEGFullRes"
    LIVE_ORIGINAL = "resOriginalVidComplRes"
    VIDEO_MEDIUM = "resVidMedRes"
    VIDEO_SMALL = "resVidSmallRes"

    def __str__(self) -> str:
        return self.name


class _FileTypeFieldName(Enum):
    ORIGINAL = "resOriginalFileType"
    ALTERNATIVE = "resOriginalAltFileType"
    MEDIUM = "resJPEGMedFileType"
    THUMB = "resJPEGThumbFileType"
    ADJUSTED = "resJPEGFullFileType"
    LIVE_ORIGINAL = "resOriginalVidComplFileType"
    VIDEO_MEDIUM = "resVidMedFileType"
    VIDEO_SMALL = "resVidSmallFileType"

    def __str__(self) -> str:
        return self.name


_VALUE_FILED_NAME = "value"
_SIZE_FILED_NAME = "size"
_URL_FILED_NAME = "downloadURL"


def _master_fields_node(
    record: _MasterRecordNode,
) -> Optional[_FieldsNode]:
    return typing.cast(Optional[_FieldsNode], record.get("fields"))


def _res_node(
    node: _ResourceFieldName,
) -> Callable[[_FieldsNode], Optional[_ResNode]]:
    def _intern(fields: _FieldsNode) -> Optional[_ResNode]:
        return typing.cast(Optional[_ResNode], fields.get(f"{node}"))

    return _intern


def _res_value_node(res: _ResNode) -> Optional[_ResValueNode]:
    return typing.cast(Optional[_ResValueNode], res.get(_VALUE_FILED_NAME))


def _res_value_size(value: _ResValueNode) -> Optional[_ResValueSize]:
    return typing.cast(Optional[_ResValueSize], value.get(_SIZE_FILED_NAME))


def _res_value_url(value: _ResValueNode) -> Optional[_ResValueURL]:
    return typing.cast(Optional[_ResValueURL], value.get(_URL_FILED_NAME))


def _file_type_node(
    node: _FileTypeFieldName,
) -> Callable[[_FieldsNode], Optional[_FileTypeNode]]:
    def _intern(fields: _FieldsNode) -> Optional[_FileTypeNode]:
        return typing.cast(Optional[_FileTypeNode], fields.get(f"{node}"))

    return _intern


def _file_type_value(value: _FileTypeNode) -> Optional[_FileType]:
    return typing.cast(Optional[_FileType], value.get(_VALUE_FILED_NAME))


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


# bvbnjhkjbnbngbg
# def _extract_size_and_url(
#     prefix: str,
#     fields: Dict[str, Any],
#     ) -> Tuple[int, str]:

#     res_name = f"{prefix}Res"
#     size = fields[res_name]['value']['size']
#     download_url = fields[res_name]['value']['downloadURL']
#     return (size, download_url)
