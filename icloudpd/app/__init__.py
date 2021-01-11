"""
    Main processor
"""

from typing import Optional, Callable, Any, Tuple
from collections.abc import Iterable #, Mapping
import os
import datetime

import itertools as it
import functools as ft

from tqdm import tqdm

import icloudpd.cloud
import icloudpd.cloud.network as net
import icloudpd.cloud.map
import icloudpd.core as core
import icloudpd.core.cloud as cloud
import icloudpd.authentication
import icloudpd.core.typing as ty
import icloudpd.util.operators as ops
import icloudpd.util.path
import icloudpd.file as file



def start( # pylint: disable=R0914,R0913
    username: str,
    album: str,
    recent: int,
    directory: str,
    folder_structure: str,
    cookie_directory: str
    ): # pragma: no cover
    """
        Main entry point for synchronizing/downloading
    """

    folder_mapper=ops.compose(
        core.folder_map_builder(folder_structure),
        lambda path: os.path.join(directory, path),
    )

    fetch_meta = ft.partial(net.fetch_meta, album)

    # strategy to fetch Photo tuple from cloud
    def fetch_builder(fetch_meta: Callable[[Any], Iterable]) -> \
        Callable[[Any], Iterable]:
        return lambda context: it.islice(
                map(
                    cloud.to_photo,
                    map(
                        icloudpd.cloud.map.to_photo_source,
                        fetch_meta(context)
                    )
                )
            ,recent)

    def ext_select_builder(ref_index: int) -> Callable[[ty.Photo], str]:
        def _ext_selector(photo):
            ext_from_type = cloud.get_ext_from_type(photo[ref_index][0])
            if ext_from_type is None:
                import pathlib # pylint: disable=C0415
                return pathlib.PurePath(photo[2]).suffix
            return ext_from_type
        return _ext_selector

    name_selector = lambda photo: photo[2]

    main_path_mapper = cloud.path_map_builder(
        folder_mapper,
        name_selector,
        ext_select_builder(3),
        )

    complimentary_path_mapper = cloud.path_map_builder(
        folder_mapper,
        cloud.get_complimentary_filename_from_main_ext,
        ext_select_builder(4),
        )

    download_ref_enqueuer = lambda photos: filter(
        lambda ref: ref[3] is not None,
        it.chain(
            map(
                lambda photo: photo[3],
                photos,
            ),
            map(
                lambda photo: photo[4],
                photos,
            ),
        )
    )

    file_ref_checker = lambda refs: filter(
        lambda ref: not os.path.exists(ref[3]),
        refs,
    )

    # download_queue_sum = lambda queue: sum(
    #     map(
    #         lambda ref: ref[1],
    #         queue
    #     )
    # )

    def folder_ensurer(refs):
        def _folder_ensurer(ref):
            file.ensure_folder(ref[3])
            return ref
        return map(
            _folder_ensurer,
            refs
        )

    authenticator = lambda _: icloudpd.authentication.authenticate(username, None, cookie_directory)

    # what should be applied to each photo
    photo_pipeline = ops.compose(
        cloud.image_path_builder(main_path_mapper, complimentary_path_mapper),
        # cloud.image_path_builder(main_path_mapper, complimentary_path_mapper),
    )

    # mock_data = [('AR60epj6EMSgX29I/gW2iDhX6taV',
    # datetime.datetime(2021, 1, 2, 20, 36, 13, 151000, tzinfo=datetime.timezone.utc),
    # 'IMG_1992.HEIC',
    # ('public.heic', 1599930,
    # 'https://cvws.icloud-content.com/B/AR60epj6EMSgX29I_gW2iDhX6taVAZYe2q8DdK9oiV3AA1s37W6F84Jo/${f}?o=Anvpy4iZQ_8XYDMcAH_kN1NHrQWYVwBLyRFHocqO-1wf&v=1&x=3&a=CAogOrIyf0gDMCqrpzbwZgMslJ217j0bkBRLno6loAqgseoSaxDN8drR7i4Yzc620-4uIgEAUgRX6taVWgSF84JoaiUJP2HEmwnQmz_WTjBTNqcY0qVMK3W6tqCTpx3CuPfSpXIirV6WciVcVht9sq-R-5dykjproM1bu5KSvLw6BlHazTGz-TZzK-KXrBGW&e=1610250823&fl=&r=0a891b79-f7a9-44fe-90cd-24a0a20c059f-1&k=nsfOYqIrLYbAI_MqpdiKZg&ckc=com.apple.photos.cloud&ckz=PrimarySync&y=1&p=39&s=vx-o0Hazi3PD4HL0lTLMEiQ-2rU'), (None, None, None))] # pylint: disable=C0301

    context = authenticator(None)

    downloader = lambda ref: file.stream_to_file(ref[3], net.fetch_file_stream(context, ref[2]))

    top_pipeline = ops.compose(
        # authenticator,
        fetch_builder(fetch_meta),
        # lambda _: mock_data,
        ft.partial(map, photo_pipeline),
        download_ref_enqueuer,
        file_ref_checker,
        folder_ensurer,
        ft.partial(map, downloader),
    )

    result = list(top_pipeline(context))

    print(f"Pipeline Result: {result}")
