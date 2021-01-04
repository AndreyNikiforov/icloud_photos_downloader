"""
    Domain-specific logic
"""
from typing import Callable
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
