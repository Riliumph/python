import abc
from typing import Any, Dict, List, Tuple

from base.presenter import BasePresenter
from user.gateway.repository import UserRepository as UserRepo


class UserReader(abc.ABC):
    @abc.abstractmethod
    def __init__(self, repo: UserRepo):
        raise NotImplementedError()

    @abc.abstractmethod
    def ReadUserById(self, data: int) -> Tuple[int, BasePresenter]:
        raise NotImplementedError()
