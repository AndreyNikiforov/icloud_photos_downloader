"""
    Domain-specific logic
"""
from typing import Callable
import datetime
import icloudpd.core.typing as ty

def folder_mapper(folder_structure: str) -> Callable[[ty.Photo], str]:
    """
        Calculates destination folder based on photo meta data
    """

    def _mapper(photo) -> str:
        return folder_structure.format(
            photo[1]
        )
    return _mapper

def make_valid_filename(source: str, length: int = 12) -> str:
    """
        Makes any string into valid file name by replacing non valid symbols and reducing length
    """
    import re   # pylint: disable=C0415
    return re.sub('[^0-9a-zA-Z]', '_', source)[0:length]

def cleanse_datetime(date_time: datetime.datetime) -> datetime.datetime:
    """
        Fixed incorrect/small dates
    """
    if date_time.year == datetime.MINYEAR and date_time.month == 1 and date_time.day == 1:
        # timestamp was built from time only
        return date_time.replace(year=1970)
    if date_time.year < 100:
        # missing epoch
        if date_time.year >= 70:
            return date_time.replace(year=1900+date_time.year)
        return date_time.replace(year=2000+date_time.year)
    return date_time
