import abc
from typing import Any, Dict, List

from sample_app.base.repository import BaseRepository

# 思いつくまま便利そうなInputPortを書いてみる


class UserCreatorIF(abc.ABC):
    @abc.abstractmethod
    def __init__(self, repo: BaseRepository) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def CreateUser(self, data: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError()

    @abc.abstractmethod
    def CreateUsers(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        raise NotImplementedError()


class UserReaderIF(abc.ABC):
    @abc.abstractmethod
    def __init__(self, repo: BaseRepository) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def ReadUserById(self, data: int):
        raise NotImplementedError()


class UserUpdaterIF(abc.ABC):
    @abc.abstractmethod
    def __init__(self, repo: BaseRepository) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def UpdateUser(self, user_id: int, data: Dict[str, Any]):
        raise NotImplementedError()

    @abc.abstractmethod
    def UpdateUsers(self, user_ids: List[int], data: List[Dict[str, Any]]):
        raise NotImplementedError()


class UserDeleterIF(abc.ABC):
    @abc.abstractmethod
    def __init__(self, repo: BaseRepository) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def DeleteUser(self, user_id: int):
        raise NotImplementedError()

    @abc.abstractmethod
    def DeleteUsers(self, user_ids: List[int]):
        raise NotImplementedError()
