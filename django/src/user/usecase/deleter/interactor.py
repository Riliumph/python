import logging
from typing import List

from user.gateway import UserRepository as UserRepo
from user.usecase.deleter import inputport

logger = logging.getLogger("app")


class UserDeleter(inputport.UserDeleter):
    def __init__(self, repo: UserRepo):
        self.repo = repo

    def DeleteUser(self, user_id: int):
        '''ユーザーを削除するビジネスロジック

        Args:
            user_id (int): ユーザーID
        '''
        logger.info("execute a delete operation",
                    extra={"details": {"user_id": user_id}})
        self.repo.delete(user_id)

    def DeleteUsers(self, user_ids: List[int]):
        '''ユーザーを一括削除するビジネスロジック
            Repositoryがdelete関数でN件削除をサポートしている。
            そのためDeleteUser関数と同じ実装だが、ビジネスロジックとしては分けておく。
        Args:
            user_ids (List[int]): ユーザーID群
        '''
        logger.info("execute delete operations",
                    extra={"details": {"user_id": user_ids}})
        self.repo.delete(user_ids)
