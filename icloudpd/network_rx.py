"""
    Transfers bytes over the wire
"""
from typing import Optional, Any, Mapping, Tuple
import rx
from rx import operators as ops

def fetch_meta(
    album: str,
    scheduler: Optional[rx.typing.Scheduler]=None) -> \
        rx.typing.Observable[Tuple[Mapping[str,Any], Mapping[str, Any]]]:
    """
        Fetch photo metadata
    """
    def _fetch_meta(source: rx.typing.Observable[Any]) -> \
        rx.typing.Observable[Tuple[Mapping[str,Any], Mapping[str, Any]]]:
        return source.pipe(
            ops.flat_map(lambda context:
                rx.from_iterable(context.photos.albums[album],
                scheduler).pipe(
                    ops.map(lambda photo: (photo._master_record, photo._asset_record)), # pylint: disable=W0212
                )
            ),
        )
    return _fetch_meta

def get_file_stream(
    context: Any,
    url: str,
    scheduler: Optional[rx.typing.Scheduler]=None) -> \
        rx.typing.Observable[bytes]:
    """
        Gets chunks of the the file
    """
    return rx.from_iterable(context.session.get(
            url,
            stream=True,
        ).iter_content(chunk_size=1024),
        scheduler
    )

def meta_len(
    album: str,
    scheduler: Optional[rx.typing.Scheduler]=None) -> \
        rx.typing.Observable[Tuple[Mapping[str,Any], Mapping[str, Any]]]:
    """
        Fetch photo metadata
    """
    def _meta_len(source: rx.typing.Observable[Any]) -> \
        rx.typing.Observable[Tuple[Mapping[str,Any], Mapping[str, Any]]]:
        return source.pipe(
            ops.map(lambda context:len(context.photos.albums[album]))
        )
    return _meta_len
