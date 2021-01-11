"""
    Access to file system
"""
from typing import Callable
from collections.abc import Iterable
import pathlib

def stream_to_file(filename: str, stream: Iterable) -> int:
    """
        Creates file and saves stream to it
        returns total size saved
    """
    with open(filename, "wb") as file:
        total = 0
        for chunk in stream:
            if chunk:
                file.write(chunk)
                total+=len(chunk)
        return total

def ensure_folder(filename: str) -> bool:
    """
        creates folder for file if not exists
        returns true if it was created
    """
    root = pathlib.Path(filename).parent
    if not root.exists():
        root.mkdir(parents=True, exist_ok=True)
        return True
    return False
