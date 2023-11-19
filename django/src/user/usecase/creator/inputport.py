import abc
from typing import Any, Dict, List

from user.gateway.repository import UserRepository as UserRepo
from user.presenter.presenter import UserPresenter


class UserCreator(abc.ABC):
    @abc.abstractmethod
    def __init__(self, repo: UserRepo):
        raise NotImplementedError()

    @abc.abstractmethod
    def CreateUser(self, data: Dict[str, Any]) -> UserPresenter:
        raise NotImplementedError()

    @abc.abstractmethod
    def CreateUsers(self, data: List[Dict[str, Any]]) -> UserPresenter:
        raise NotImplementedError()
