"""
    Loads metadata
"""
from typing import Any, Mapping, Tuple, Iterable, Callable
import collections.abc
import itertools as it

import icloudpd.util

def _get(
    source: Mapping[str, Any],
    paths: Iterable[str]) -> Iterable[Any]:
    """
        Get hierarchy from dict represented by path
    """
    if paths:
        if isinstance(source, collections.abc.Mapping):
            yield from _get(source.get(paths[0]), paths[1:])
        else:
            pass    # did not find
    else:
        yield source

def _get_id(source: Tuple[Mapping[str, Any], Mapping[str, Any]]) -> Iterable[str]:
    """
        Gets ID of the photo
    """
    (master_record, _) = source
    yield from _get(
            master_record, ["recordName"]
        )

def _get_url_adjustment(
    source: Tuple[Mapping[str, Any], Mapping[str, Any]]) -> Iterable[Tuple]:
    """
        Gets url meta data (type, size, link) for adjusted image
    """
    (_, asset_record) = source
    yield from  filter(
        lambda triplet: len(triplet) == 3,
        icloudpd.util.buffer_with_count(
            3,
            it.chain(
                _get(asset_record, ["fields", "resJPEGFullFileType", "value"]),
                _get(asset_record, ["fields", "resJPEGFullRes", "value", "size"]),
                _get(asset_record, ["fields", "resJPEGFullRes", "value", "downloadURL"]),
            )
        )
    )

def _get_url_original(
    source: Tuple[Mapping[str, Any], Mapping[str, Any]]) -> Iterable[Tuple]:
    """
        Gets url meta data (type, size, link) for original image/video
    """
    (master_record, _) = source
    yield from  filter(
        lambda triplet: len(triplet) == 3,
        icloudpd.util.buffer_with_count(
            3,
            it.chain(
                _get(master_record, ["fields", "resOriginalFileType", "value"]),
                _get(master_record, ["fields", "resOriginalRes", "value", "size"]),
                _get(master_record, ["fields", "resOriginalRes", "value", "downloadURL"]),
            )
        )
    )

def _get_url_complimentary(
    source: Tuple[Mapping[str, Any], Mapping[str, Any]]) -> Iterable[Tuple]:
    """
        Gets url meta data (type, size, link) for complimentary video
    """
    (master_record, _) = source
    yield from  filter(
        lambda triplet: len(triplet) == 3,
        icloudpd.util.buffer_with_count(
            3,
            it.chain(
                _get(master_record, ["fields", "resOriginalVidComplFileType", "value"]),
                _get(master_record, ["fields", "resOriginalVidComplRes", "value", "size"]),
                _get(master_record, ["fields", "resOriginalVidComplRes", "value", "downloadURL"]),
            )
        )
    )

def _get_filename(source: Tuple[Mapping[str, Any], Mapping[str, Any]]) -> Iterable[str]:

    (master_record, _) = source

    import base64 # pylint: disable=C0415

    yield from map(
        lambda x: base64.b64decode(x).decode('utf-8'),
        _get(
            master_record,
            ["fields", "filenameEnc", "value"]
        ),
    )

def _get_asset_timestamp(source: Tuple[Mapping[str, Any], Mapping[str, Any]]) -> Iterable[int]:

    (_, asset_record) = source

    yield from _get(
        asset_record,
        ["fields", "assetDate", "value"]
    )

def filename_default_to_id(source) -> Iterable[str]:
    """
        Strategy for selecting filename and falling back to id-based file name
    """

    yield from it.islice(
        it.chain(
            _get_filename(source),
            map(
                icloudpd.util.make_valid_filename,
                _get_id(source),
            )
        ),
        1,
    )

def timestamp_default_zero(source) -> Iterable[int]:
    """
        Takes asset date as timestamp and fallsback to 0
    """
    yield from it.islice(
        it.chain(
            _get_asset_timestamp(source),
            icloudpd.util.once(0),
        ),
        1,
    )

def url_adjustment_default_to_original(source) -> Iterable[Iterable[Any]]:
    """
        Strategy that takes adjustment meta (type, size, url) and falls back to original
        Adjustments are portrait photos and edits
    """
    yield from it.islice(
        it.chain(
            _get_url_adjustment(source),
            _get_url_original(source),
        ),
        1,
    )

def load( # pylint: disable=R0913
    source: Tuple[Mapping[str, Any], Mapping[str, Any]],
    id_strategy: Callable[[Tuple[Mapping[str, Any], Mapping[str, Any]]], Iterable[str]] = _get_id,
    timestamp_strategy:
        Callable[
            [Tuple[Mapping[str, Any], Mapping[str, Any]]],
            Iterable[int]
        ] = timestamp_default_zero,
    filename_strategy:
        Callable[
            [Tuple[Mapping[str, Any], Mapping[str, Any]]],
            Iterable[str]
        ] = filename_default_to_id,
    main_url_strategy:
        Callable[
            [Tuple[Mapping[str, Any], Mapping[str, Any]]],
            Iterable[Iterable[Any]]
        ] = url_adjustment_default_to_original,
    complimentary_url_strategy:
        Callable[
            [Tuple[Mapping[str, Any], Mapping[str, Any]]],
            Iterable[Iterable[Any]]
        ] = _get_url_complimentary,
    ) -> Iterable:
    """
        Loads asset attributes from tuple of records into Asset object
    """

    yield from icloudpd.util.buffer_with_count(
        5,
        it.chain(
            id_strategy(source),
            timestamp_strategy(source),
            filename_strategy(source),
            main_url_strategy(source),
            complimentary_url_strategy(source),
        ),
    )
