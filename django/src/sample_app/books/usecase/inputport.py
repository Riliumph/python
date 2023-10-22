import abc
from typing import Any, Dict, List

from base.gateway import BaseRepository

# 思いつくまま便利そうなInputPortを書いてみる


class BookCreatorIF(abc.ABC):
    @abc.abstractmethod
    def __init__(self, repo: BaseRepository) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def CreateBook(self, data: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError()

    @abc.abstractmethod
    def CreateBooks(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        raise NotImplementedError()


class GiveGenreToBookIF(abc.ABC):
    @abc.abstractmethod
    def __init__(self, repo: BaseRepository) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def GiveGenre(self, book_id: int, genre: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError()
