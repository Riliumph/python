import abc
from typing import Any, Dict, List

from base.presenter import BasePresenter
from user_mng_app.gateway.repository import UserRepository as UserRepo


class UserCreator(abc.ABC):
    @abc.abstractmethod
    def __init__(self, repo: UserRepo):
        raise NotImplementedError()

    @abc.abstractmethod
    def CreateUser(self, data: Dict[str, Any]) -> BasePresenter:
        raise NotImplementedError()

    @abc.abstractmethod
    def CreateUsers(self, data: List[Dict[str, Any]]) -> BasePresenter:
        raise NotImplementedError()
