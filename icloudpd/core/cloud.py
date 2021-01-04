"""
    Strategies for cleaning and selecting incoming data
"""
from typing import Callable
import datetime

import icloudpd.core.typing as ty
import icloudpd.core

def filename_default_to_id(photo: ty.PhotoSource) -> str:
    """
        Strategy for selecting filename and falling back to id-based file name
    """

    value = photo[2]
    return icloudpd.core.make_valid_filename(photo[0]) if value is None else value

def timestamp_default_zero(photo: ty.PhotoSource) -> int:
    """
        Takes asset date as timestamp and fallsback to 0
    """
    value = photo[1]
    return 0 if value is None else value

def datetime_cleansed(timestamp_ms: int) -> datetime.datetime:
    """
        Takes asset date as timestamp in ms and fallsback to 0
    """
    date_time = datetime.datetime.fromtimestamp(timestamp_ms / 1000, tz=datetime.timezone.utc)
    if date_time.year == datetime.MINYEAR and date_time.month == 1 and date_time.day == 1:
        # timestamp was built from time only
        return date_time.replace(year=1970)
    if date_time.year < 100:
        # missing epoch
        if date_time.year >= 70:
            return date_time.replace(year=1900+date_time.year)
        return date_time.replace(year=2000+date_time.year)
    return date_time

def url_adjustment_default_to_original(photo: ty.PhotoSource) -> ty.Photo:
    """
        Strategy that takes adjustment meta (type, size, url) and falls back to original
        Adjustments are portrait photos and edits
    """
    value = photo[3]
    fallback = photo[4]
    return fallback if value is None else value

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
        ] = lambda s: datetime_cleansed(timestamp_default_zero(s)),
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
        ] = lambda x: x[5],
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
