"""
    Loads metadata
"""
from typing import Optional, Any, Mapping, Tuple
import collections.abc
import rx
from rx import operators as ops

def _get(
    source: Mapping[str, Any],
    *paths: str,
    scheduler: Optional[rx.typing.Scheduler]=None) -> rx.typing.Observable:
    """
        Get hierarchy from dict represented by path

    """
    if len(paths) == 0:
        return rx.return_value(source, scheduler)
    if not isinstance(source, collections.abc.Mapping):
        return rx.empty(scheduler)
    node = source.get(paths[0])
    return _get(node, *paths[1:])

def _get_id(
    source: Tuple[Mapping[str, Any],
    Mapping[str, Any]],
    scheduler: Optional[rx.typing.Scheduler]=None) -> rx.typing.Observable:
    """
        Gets ID of the photo
    """
    def _of(*args):
        return rx.from_iterable(args, scheduler).pipe(
            ops.flat_map(lambda x: _get(*x, scheduler=scheduler)),
        )
    (master_record, _) = source
    return _of(
            (master_record, "recordName")
        )

def _get_url(
    source: Tuple[Mapping[str, Any],
    Mapping[str, Any]],
    scheduler: Optional[rx.typing.Scheduler]=None) -> rx.typing.Observable:
    """
        Gets url meta data (type, size, link)
    """
    def _dict_list(list_of_dictionaries):
        """
            Convert list of maps {index:value} to the list of ordered values
        """
        inter_dictionary = dict()
        for dictionary in list_of_dictionaries:
            (key,value) = list(dictionary.items())[0]
            inter_dictionary[key] = value
        for i in range(len(inter_dictionary)):  # pylint: disable=C0200
            yield inter_dictionary[i]

    def _of(*args):
        return rx.from_iterable(args, scheduler).pipe(
            # flat_map does not guarantee order, so we have to deal with indexes, dict
            ops.flat_map_indexed(
                lambda x, i: _get(*x, scheduler=scheduler).pipe(
                    ops.map(lambda v: {i: v})
                    )
                ),
            ops.buffer_with_count(3),
            ops.map(lambda x: list(_dict_list(x))),
            ops.filter(lambda x: len(x) == 3),
        )
    (master_record, asset_record) = source
    return _of(
            (asset_record, "fields", "resJPEGFullFileType", "value"),
            (asset_record, "fields", "resJPEGFullRes", "value", "size"),
            (asset_record, "fields", "resJPEGFullRes", "value", "downloadURL"),
        ).pipe(
            ops.concat(
                _of(
                    (master_record, "fields", "resOriginalFileType", "value"),
                    (master_record, "fields", "resOriginalRes", "value", "size"),
                    (master_record, "fields", "resOriginalRes", "value", "downloadURL"),
                ),
                _of(
                    (master_record, "fields", "resOriginalFileType", "value"),
                    (master_record, "fields", "resOriginalRes", "value", "size"),
                    (master_record, "fields", "resOriginalRes", "value", "downloadURL"),
                ),
            ),
            ops.take(1)
        )

def _get_filename(
    source: Tuple[Mapping[str, Any],
    Mapping[str, Any]],
    scheduler: Optional[rx.typing.Scheduler]=None) -> rx.typing.Observable:

    def _of(*args):
        return rx.from_iterable(args, scheduler).pipe(
            ops.flat_map(lambda x: _get(*x, scheduler=scheduler)),
        )

    (master_record, _) = source

    import re   # pylint: disable=C0415
    import base64 # pylint: disable=C0415

    return _of(
        (master_record, "fields", "filenameEnc", "value"),
    ).pipe(
        ops.map(lambda x: base64.b64decode(x).decode('utf-8')),
        ops.concat(_get_id(source, scheduler).pipe(
                ops.map(lambda x: re.sub('[^0-9a-zA-Z]', '_', x)[0:12]),
            )
        ),
        ops.take(1),
    )

def _get_asset_date(
    source: Tuple[Mapping[str, Any],
    Mapping[str, Any]],
    scheduler: Optional[rx.typing.Scheduler]=None) -> rx.typing.Observable:

    def _of(*args):
        return rx.from_iterable(args, scheduler).pipe(
            ops.flat_map(lambda x: _get(*x, scheduler=scheduler)),
        )

    (_, asset_record) = source

    return _of(
        (asset_record, "fields", "assetDate", "value"),
    ).pipe(
        ops.concat(rx.return_value(0, scheduler)),
        ops.take(1),
    )

def load(
    source: rx.typing.Observable[Tuple[Mapping[str, Any], Mapping[str, Any]]],
    scheduler: Optional[rx.typing.Scheduler] = None) -> rx.typing.Observable:
    """
        Loads asset attributes from tuple of records into Asset object
    """
    return source.pipe(
        ops.flat_map(lambda x: rx.empty().pipe(
                ops.concat(
                    _get_id(x, scheduler),
                    _get_asset_date(x, scheduler),
                    _get_filename(x, scheduler),
                    _get_url(x, scheduler),
                ),
                ops.buffer_with_count(4),
            ),
        ),
    )
