"""
    Transfers bytes over the wire from iCloud service
"""
from typing import Optional, Any, Mapping, Tuple, Iterable

def fetch_meta(
    album: str,
    context: Any,
    ) -> \
        Iterable[Tuple[Mapping[str,Any], Mapping[str, Any]]]:
    """
        Fetch photo metadata
    """
    yield from map(
        lambda photo: (photo._master_record, photo._asset_record), # pylint: disable=W0212
        context.photos.albums[album],
    )

def fetch_file_stream(
    context: Any,
    url: str,
    chunk_size=1024) -> Iterable[bytes]:
    """
        Gets chunks of the the file
    """
    yield from context.session.get(
        url,
        stream=True,
    ).iter_content(chunk_size=chunk_size)

def fetch_meta_len(
    album: str,
    context:Any,
    ) -> int:
    """
        Fetch photo metadata
    """
    return len(context.photos.albums[album])
