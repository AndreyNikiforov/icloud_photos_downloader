#!/usr/bin/env python
"""Main processor"""

from typing import Optional, Callable, Any
from collections.abc import Iterable, Mapping
import os

import rx
from rx import operators as ops

import icloudpd.network
import icloudpd.storage
import icloudpd.meta_rx
import icloudpd.domain
import icloudpd.authentication

def start(username:str, album: str, directory: str, folder_structure: str):
    """
        Main entry point
    """
    import os
    folder_mapper=icloudpd.domain.folder_mapper(folder_structure)
    from tqdm import tqdm
    with tqdm() as c:
        with tqdm() as t:
            _context = rx.return_value(icloudpd.authentication.authenticate(username, None))
            _photos = _context.pipe(
                ops.do(
                        rx.core.Observer(lambda photo: c.update())
                    ),
                icloudpd.network.fetch_meta(album),
                icloudpd.meta_rx.load(),
                ops.do(
                        rx.core.Observer(lambda photo: t.update())
                    ),
                # choose file location
                ops.map(lambda photo: (os.path.join(folder_mapper(photo), photo[2]), *photo)),
                ops.filter(lambda path_photo: not os.path.exists(path_photo[0])),
            )
            _downloads = _photos.pipe(
                # ops.map(lambda photo: photo[0]),
                ops.combine_latest(
                    _context
                ),
                # ops.do(
                #         rx.core.Observer(lambda photo: t.update())
                #     ),
                ops.take(10),
            )
            return _downloads.pipe(
                ops.to_iterable()
            ).run()
