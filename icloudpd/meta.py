"""
    Loads metadata
"""
from typing import Any, Mapping, Tuple, Iterable, Callable, Optional
import collections.abc

import icloudpd.util

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
    triplet = (
                _get(asset_record, ["fields", "resJPEGFullFileType", "value"]),
                _get(asset_record, ["fields", "resJPEGFullRes", "value", "size"]),
                _get(asset_record, ["fields", "resJPEGFullRes", "value", "downloadURL"]),
            )
    if all(map(lambda x: x is not None, triplet)):
        return triplet
    return None

def _get_url_original(
    source: Tuple[Mapping[str, Any], Mapping[str, Any]]) -> Optional[Tuple[str, int, str]]:
    """
        Gets url meta data (type, size, link) for original image/video
    """
    (master_record, _) = source
    triplet = (
                _get(master_record, ["fields", "resOriginalFileType", "value"]),
                _get(master_record, ["fields", "resOriginalRes", "value", "size"]),
                _get(master_record, ["fields", "resOriginalRes", "value", "downloadURL"]),
            )
    if all(map(lambda x: x is not None, triplet)):
        return triplet
    return None

def _get_url_complimentary(
    source: Tuple[Mapping[str, Any], Mapping[str, Any]]) -> Optional[Tuple[str, int, str]]:
    """
        Gets url meta data (type, size, link) for complimentary video
    """
    (master_record, _) = source
    triplet = (
                _get(master_record, ["fields", "resOriginalVidComplFileType", "value"]),
                _get(master_record, ["fields", "resOriginalVidComplRes", "value", "size"]),
                _get(master_record, ["fields", "resOriginalVidComplRes", "value", "downloadURL"]),
            )
    if all(map(lambda x: x is not None, triplet)):
        return triplet
    return None

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

def filename_default_to_id(source) -> str:
    """
        Strategy for selecting filename and falling back to id-based file name
    """

    value = _get_filename(source)
    return icloudpd.util.make_valid_filename(_get_id(source)) if value is None else value

def timestamp_default_zero(source) -> int:
    """
        Takes asset date as timestamp and fallsback to 0
    """
    value = _get_asset_timestamp(source)
    return 0 if value is None else value

def url_adjustment_default_to_original(source) -> Tuple[str, int, str]:
    """
        Strategy that takes adjustment meta (type, size, url) and falls back to original
        Adjustments are portrait photos and edits
    """
    value = _get_url_adjustment(source)
    return _get_url_original(source) if value is None else value

def load( # pylint: disable=R0913
    source: Tuple[Mapping[str, Any], Mapping[str, Any]],
    id_strategy: Callable[[Tuple[Mapping[str, Any], Mapping[str, Any]]], str] = _get_id,
    timestamp_strategy:
        Callable[
            [Tuple[Mapping[str, Any], Mapping[str, Any]]],
            int
        ] = timestamp_default_zero,
    filename_strategy:
        Callable[
            [Tuple[Mapping[str, Any], Mapping[str, Any]]],
            str
        ] = filename_default_to_id,
    main_url_strategy:
        Callable[
            [Tuple[Mapping[str, Any], Mapping[str, Any]]],
            Tuple[str, int, str]
        ] = url_adjustment_default_to_original,
    complimentary_url_strategy:
        Callable[
            [Tuple[Mapping[str, Any], Mapping[str, Any]]],
            Tuple[str, int, str]
        ] = _get_url_complimentary,
    ) -> Tuple:
    """
        Loads asset attributes from tuple of records into Asset object
    """

    return (
        id_strategy(source),
        timestamp_strategy(source),
        filename_strategy(source),
        main_url_strategy(source),
        complimentary_url_strategy(source),
    )
