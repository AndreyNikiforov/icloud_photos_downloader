"""
    Loads metadata
"""
from typing import Any, Mapping, Tuple, Iterable
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

def _get_fallback_filename(source: Tuple[Mapping[str, Any], Mapping[str, Any]]) -> Iterable[str]:
    import re   # pylint: disable=C0415
    yield from map(
        lambda x: re.sub('[^0-9a-zA-Z]', '_', x)[0:12],
        _get_id(source)
    )

def _get_asset_timestamp(source: Tuple[Mapping[str, Any], Mapping[str, Any]]) -> Iterable[int]:

    (_, asset_record) = source

    yield from _get(
        asset_record,
        ["fields", "assetDate", "value"]
    )


def load(source: Tuple[Mapping[str, Any], Mapping[str, Any]]) -> \
    Iterable:
    """
        Loads asset attributes from tuple of records into Asset object
    """

    def _once(i):
        yield i

    yield from icloudpd.util.buffer_with_count(
        5,
        it.chain(
            _get_id(source),
            it.islice(
                it.chain(
                    _get_asset_timestamp(source),
                    _once(0),
                ),
                1,
            ),
            it.islice(
                it.chain(
                    _get_filename(source),
                    _get_fallback_filename(source),
                ),
                1,
            ),
            it.islice(
                it.chain(
                    _get_url_adjustment(source),
                    _get_url_original(source),
                ),
                1,
            ),
            _get_url_complimentary(source),
        ),
    )
