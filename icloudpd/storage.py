"""
    Interface to persistent storage
"""
from typing import Optional #, Any, Mapping, Tuple
# import collections.abc
import rx
from rx import operators as ops

def save_file(
    path: str,
    chunk_factory: rx.typing.Callable[[Optional[rx.typing.Scheduler]], rx.typing.Observable[bytes]],
    scheduler: Optional[rx.typing.Scheduler] = None) -> rx.typing.Observable:
    """
        Saves stream of byte chunks as new file
    """
    class _WithFile(rx.typing.Disposable):
        """
            Wrapper for file writing
        """
        def __init__(self, path: str):
            self.path = path
            self.file = open(path, "wb")

        def dispose(self) -> None:
            self.file.close()

        def write(self, chunk: bytes) -> None:
            """
                Writes chunk to manager file
            """
            self.file.write(chunk)

    return rx.using(
        lambda: _WithFile(path),
        lambda r: chunk_factory(scheduler).pipe(
            ops.do(
                rx.core.Observer(r.write)
            ),
            ops.ignore_elements(),
        )
    ).pipe(
        ops.concat(
            rx.return_value(path, scheduler)
        )
    )
