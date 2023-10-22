import abc
from typing import Any, Dict, List, Tuple

from user.gateway import UserRepository as UserRepo
from user.presenter import UserPresenter


class UserReader(abc.ABC):
    @abc.abstractmethod
    def __init__(self, repo: UserRepo):
        raise NotImplementedError()

    @abc.abstractmethod
    def ReadUserById(self, data: int) -> Tuple[int, UserPresenter]:
        raise NotImplementedError()
