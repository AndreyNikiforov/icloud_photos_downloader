"""
    Domain-specific logic
"""
from typing import Optional, Any, Mapping, Tuple, Callable
# import rx
# from rx import operators as ops

def folder_mapper(folder_structure: str) -> Callable[[Tuple], str]:
    """
        Calculates destination folder based on photo meta data
    """

    import datetime # pylint: disable=C0415

    def _mapper(photo: Tuple[Any]) -> str:
        return folder_structure.format(
            datetime.datetime.fromtimestamp(photo[1]/1000, tz=datetime.timezone.utc)
        )
    return _mapper


# def calc_folder(folder_structure: str) -> \
#     rx.typing.Callable[[rx.typing.Observable], rx.typing.Observable]:


#     def _calc_folder(source: rx.typing.Observable[Tuple]) -> \
#         rx.typing.Observable[str]:
#         return source.pipe(
#             ops.map(calc_folder_mapper(folder_structure)),
#         )
#     return _calc_folder
