"""
    Types used set in core and used by all modules
"""

from typing import Tuple, Optional
import datetime

PhotoId = str
AssetDate = datetime.datetime
FileName = str
ReferenceSource = Tuple[Optional[str], Optional[int], Optional[str]]

AssetTimestamp = int

PhotoSource = Tuple[
    PhotoId,
    AssetTimestamp,
    FileName,
    ReferenceSource,
    ReferenceSource,
    ReferenceSource
]

Reference = Tuple[str, int, str]
Photo = Tuple[PhotoId, AssetDate, FileName, Reference, ReferenceSource]

PathReference = Tuple[str, int, str, Optional[str]]

PhotoPath = Tuple[
    PhotoId,
    AssetTimestamp,
    FileName,
    PathReference,
    PathReference,
]
