import abc
from typing import List

from user_mng_app.gateway.repository import UserRepository as UserRepo


class UserDeleter(abc.ABC):
    @abc.abstractmethod
    def __init__(self, repo: UserRepo):
        raise NotImplementedError()

    @abc.abstractmethod
    def DeleteUser(self, user_id: int):
        raise NotImplementedError()

    @abc.abstractmethod
    def DeleteUsers(self, user_ids: List[int]):
        raise NotImplementedError()
