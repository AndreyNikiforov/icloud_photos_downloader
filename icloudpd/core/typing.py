"""
    Types used set in core and used by all modules
"""

from typing import Tuple, Optional
import datetime

PhotoId = str
AssetDate = datetime.datetime
FileName = str
Reference = Tuple[str, int, str]
Photo = Tuple[PhotoId, AssetDate, FileName, Reference, Optional[Reference]]

AssetTimestamp = int
ReferenceSource = Tuple[Optional[str], Optional[int], Optional[str]]

PhotoSource = Tuple[
    PhotoId,
    AssetTimestamp,
    FileName,
    Optional[ReferenceSource],
    Optional[ReferenceSource],
    Optional[ReferenceSource]
]
