"""
    Strategies for cleaning and selecting incoming data
"""
from typing import Callable
import datetime
import functools as ft
import icloudpd.core.typing as ty
import icloudpd.core as core
import icloudpd.util.operators as ops

def filename_default_to_id(photo: ty.PhotoSource) -> str:
    """
        Strategy for selecting filename and falling back to id-based file name
    """

    value = photo[2]
    return core.make_valid_filename(photo[0]) if value is None else value

def url_adjustment_default_to_original(photo: ty.PhotoSource) -> ty.ReferenceSource:
    """
        Strategy that takes adjustment meta (type, size, url) and falls back to original
        Adjustments are portrait photos and edits
    """
    value = ops.all_or_none()(photo[3])
    fallback = photo[4]
    return fallback if value is None else value
    # return ops.compose(
    #     lambda source: source[3],
    #     ops.all_or_none,
    #     ops.default_if_none(photo[4])
    # )(
    #     photo
    # )

def timestamp_to_datetime(source: ty.PhotoSource) -> datetime.datetime:
    """
        Strategy for converting timestamp to datetime
    """
    return ops.compose(
        ops.default_if_none(0),
        lambda x: x / 1000, # convert to seconds
        ft.partial(datetime.datetime.fromtimestamp, tz=datetime.timezone.utc),
        core.cleanse_datetime,
    )(
        source[1]
    )

def to_photo( # pylint: disable=R0913
    source: ty.PhotoSource,
    id_strategy:
        Callable[
            [ty.PhotoSource],
            str
        ] = lambda x: x[0],
    datetime_strategy:
        Callable[
            [ty.PhotoSource],
            datetime.datetime
        ] = timestamp_to_datetime,
    filename_strategy:
        Callable[
            [ty.PhotoSource],
            str
        ] = filename_default_to_id,
    main_url_strategy:
        Callable[
            [ty.PhotoSource],
            ty.Reference,
        ] = url_adjustment_default_to_original,
    complimentary_url_strategy:
        Callable[
            [ty.PhotoSource],
            ty.Reference,
        ] = lambda x: ops.all_or_none()(x[5]),
    ) -> ty.Photo:
    """
        Loads asset attributes from source type into core Photo type applying
        cleansing and selection strategies
    """

    return (
        id_strategy(source),
        datetime_strategy(source),
        filename_strategy(source),
        main_url_strategy(source),
        complimentary_url_strategy(source),
    )
