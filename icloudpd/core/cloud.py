"""
    Strategies for cleaning and selecting incoming data
"""
from typing import Callable, Union
import datetime
import functools as ft
import icloudpd.core.typing as ty
import icloudpd.core as core
import icloudpd.util.operators as ops

def filename_default_to_id(photo: ty.PhotoSource) -> str:
    """
        Strategy for selecting filename and falling back to id-based file name
    """

    value = photo[2]
    return core.make_valid_filename(photo[0]) if value is None else value

def url_adjustment_default_to_original(photo: ty.PhotoSource) -> ty.ReferenceSource:
    """
        Strategy that takes adjustment meta (type, size, url) and falls back to original
        Adjustments are portrait photos and edits
    """
    value = ops.all_or_none()(photo[3])
    fallback = photo[4]
    return fallback if value is None else value
    # return ops.compose(
    #     lambda source: source[3],
    #     ops.all_or_none,
    #     ops.default_if_none(photo[4])
    # )(
    #     photo
    # )

def timestamp_to_datetime(source: ty.PhotoSource) -> datetime.datetime:
    """
        Strategy for converting timestamp to datetime
    """
    return ops.compose(
        ops.default_if_none(0),
        lambda x: x / 1000, # convert to seconds
        ft.partial(datetime.datetime.fromtimestamp, tz=datetime.timezone.utc),
        core.cleanse_datetime,
    )(
        source[1]
    )

def set_complimentary_url_none_if_any(photo: ty.PhotoSource) -> ty.ReferenceSource:
    """
        If any of the fields in compl url block are None then all elements are set None
    """
    return ops.compose(
            lambda photo: photo[5],
            ops.all_or_none(),
            ops.default_if_none((None, None, None))
        )(photo)

def to_photo( # pylint: disable=R0913
    source: ty.PhotoSource,
    id_strategy:
        Callable[
            [ty.PhotoSource],
            str
        ] = lambda x: x[0],
    datetime_strategy:
        Callable[
            [ty.PhotoSource],
            datetime.datetime
        ] = timestamp_to_datetime,
    filename_strategy:
        Callable[
            [ty.PhotoSource],
            str
        ] = filename_default_to_id,
    main_url_strategy:
        Callable[
            [ty.PhotoSource],
            ty.Reference,
        ] = url_adjustment_default_to_original,
    complimentary_url_strategy:
        Callable[
            [ty.PhotoSource],
            ty.ReferenceSource,
        ] = set_complimentary_url_none_if_any
    ) -> ty.Photo:
    """
        Loads asset attributes from source type into core Photo type applying
        cleansing and selection strategies
    """

    return (
        id_strategy(source),
        datetime_strategy(source),
        filename_strategy(source),
        main_url_strategy(source),
        complimentary_url_strategy(source),
    )

def get_ext_from_type(filetype) -> str:
    """
        Select extension suffix of the file based on file type
        None if unknown
    """
    ext_map = {
        u"public.heic": u".HEIC",
        u"public.jpeg": u".JPG",
        u"public.png": u".PNG",
        u"com.apple.quicktime-movie": u".MOV"
    }

    return ext_map.get(filetype)

def get_complimentary_filename_from_main_ext(photo: ty.Photo) -> str:
    """
        change complimentary filename based on other photo elements
        e.g. add original extention to the name: IMG_1234_HEIC.MOV
    """
    import pathlib # pylint: disable=C0415
    filename = photo[2]
    path = pathlib.PurePath(filename)
    main_ext = get_ext_from_type(photo[3][0])[1:]
    name = f"{path.stem}_{main_ext}"
    return str(path.with_name(name).with_suffix(path.suffix))

def image_path_builder(main_path_mapper, complimentary_path_mapper) -> \
    Callable[[Union[ty.Photo, ty.PhotoPath]], ty.PhotoPath]:
    """
        Calculates paths for assets
    """
    return lambda photo: (
        photo[0],
        photo[1],
        photo[2],
        ops.compose(
            ops.all_or_none(),
            ops.default_if_none((None, None, None, None)),
        )(
            (
                photo[3][0],
                photo[3][1],
                photo[3][2],
                main_path_mapper(photo),
            )
        ),
        ops.compose(
            ops.all_or_none(),
            ops.default_if_none((None, None, None, None)),
        )(
            (
                photo[4][0],
                photo[4][1],
                photo[4][2],
                complimentary_path_mapper(photo),
            )
        ),
    )

def path_map_builder(
    root_selector: Callable[[Union[ty.Photo, ty.PhotoPath]], str],
    stem_selector: Callable[[Union[ty.Photo, ty.PhotoPath]], str],
    suffix_selector: Callable[[Union[ty.Photo, ty.PhotoPath]], str],
    ) -> Callable[[Union[ty.Photo, ty.PhotoPath]], str]:
    """
        Build mapper from Photo or PhotoPath to full path
    """
    def _path_map_builder(photo):
        root = root_selector(photo)
        stem = stem_selector(photo)
        suffix = suffix_selector(photo)
        import os   # pylint: disable=C0415
        import icloudpd.util.path # pylint: disable=C0415
        return os.path.join(root, icloudpd.util.path.set_ext(stem, suffix))
    return _path_map_builder
