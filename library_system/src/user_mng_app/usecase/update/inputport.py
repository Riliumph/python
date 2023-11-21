import abc
from typing import Any, Dict, List

from base.presenter import BasePresenter
from user_mng_app.gateway.repository import UserRepository as UserRepo


class UserUpdater(abc.ABC):
    @abc.abstractmethod
    def __init__(self, repo: UserRepo):
        raise NotImplementedError()

    @abc.abstractmethod
    def UpdateUser(self, user_id: int, data: Dict[str, Any]):
        raise NotImplementedError()

    @abc.abstractmethod
    def UpdateUsers(self, user_ids: List[int], data: List[Dict[str, Any]]):
        raise NotImplementedError()
