"""
    Maps wire-level metadata to fields
"""
from typing import Any, Mapping, Tuple, Iterable, Callable, Optional
import collections.abc, datetime

import icloudpd.util

import icloudpd.core.typing

def _get(
    source: Mapping[str, Any],
    paths: Iterable[str]) -> Optional[Any]:
    """
        Get hierarchy from dict represented by path
    """
    if paths:
        if isinstance(source, collections.abc.Mapping):
            return _get(source.get(paths[0]), paths[1:])
        return None
    return source

def _get_id(source: Tuple[Mapping[str, Any], Mapping[str, Any]]) -> str:
    """
        Gets ID of the photo
    """
    (master_record, _) = source
    return _get(
            master_record, ["recordName"]
        )

def _get_url_adjustment(
    source: Tuple[Mapping[str, Any], Mapping[str, Any]]) -> Optional[Tuple[str, int, str]]:
    """
        Gets url meta data (type, size, link) for adjusted image
    """
    (_, asset_record) = source
    return (
                _get(asset_record, ["fields", "resJPEGFullFileType", "value"]),
                _get(asset_record, ["fields", "resJPEGFullRes", "value", "size"]),
                _get(asset_record, ["fields", "resJPEGFullRes", "value", "downloadURL"]),
            )

def _get_url_original(
    source: Tuple[Mapping[str, Any], Mapping[str, Any]]) -> Optional[Tuple[str, int, str]]:
    """
        Gets url meta data (type, size, link) for original image/video
    """
    (master_record, _) = source
    return (
                _get(master_record, ["fields", "resOriginalFileType", "value"]),
                _get(master_record, ["fields", "resOriginalRes", "value", "size"]),
                _get(master_record, ["fields", "resOriginalRes", "value", "downloadURL"]),
            )

def _get_url_complimentary(
    source: Tuple[Mapping[str, Any], Mapping[str, Any]]) -> Optional[Tuple[str, int, str]]:
    """
        Gets url meta data (type, size, link) for complimentary video
    """
    (master_record, _) = source
    return (
                _get(master_record, ["fields", "resOriginalVidComplFileType", "value"]),
                _get(master_record, ["fields", "resOriginalVidComplRes", "value", "size"]),
                _get(master_record, ["fields", "resOriginalVidComplRes", "value", "downloadURL"]),
            )

def _get_filename(source: Tuple[Mapping[str, Any], Mapping[str, Any]]) -> Optional[str]:
    (master_record, _) = source
    filename = _get(
            master_record,
            ["fields", "filenameEnc", "value"]
        )
    if filename is not None:
        import base64 # pylint: disable=C0415
        return base64.b64decode(filename).decode('utf-8')
    return None

def _get_asset_timestamp(source: Tuple[Mapping[str, Any], Mapping[str, Any]]) -> Optional[int]:
    (_, asset_record) = source
    return _get(
        asset_record,
        ["fields", "assetDate", "value"]
    )

def to_photo_source(
    source: Tuple[Mapping[str, Any], Mapping[str, Any]]) -> icloudpd.core.typing.PhotoSource:
    """
        Loads asset attributes from metadata into PhotoSource type
    """

    return (
        _get_id(source),
        _get_asset_timestamp(source),
        _get_filename(source),
        _get_url_adjustment(source),
        _get_url_original(source),
        _get_url_complimentary(source),
    )
