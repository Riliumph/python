import abc
from typing import Any, Dict, List

from base.gateway import BaseRepository


class GiveGenreToBookIF(abc.ABC):
    @abc.abstractmethod
    def __init__(self, repo: BaseRepository) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def GiveGenre(self, book_id: int, genre: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError()
