import abc
from typing import Any, Dict, List, Tuple

from user.gateway.repository import UserRepository as UserRepo
from user.presenter.presenter import UserPresenter


class UserReader(abc.ABC):
    @abc.abstractmethod
    def __init__(self, repo: UserRepo):
        raise NotImplementedError()

    @abc.abstractmethod
    def ReadUserById(self, data: int) -> Tuple[int, UserPresenter]:
        raise NotImplementedError()
