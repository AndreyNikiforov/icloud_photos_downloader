"""
    Different Utils
"""

import os
import tempfile
import errno
import sys

import itertools

def buffer_with_count(count, iterable):
    """
        Buffer from iterator n-th items
        from: https://stackoverflow.com/questions/8991506/iterate-an-iterator-by-chunks-of-n-in-python
    """  # pylint: disable=C0301
    it = iter(iterable) # pylint: disable=C0103
    while True:
        chunk = tuple(itertools.islice(it, count))
        if not chunk:
            return
        yield chunk

def once(i):
    """
        Generator with just one value
    """
    yield i
