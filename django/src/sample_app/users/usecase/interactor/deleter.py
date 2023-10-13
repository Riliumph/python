import logging
from typing import Any, Dict, List

from django.forms.models import model_to_dict

from sample_app.users.repository import UserRepository
from sample_app.users.usecase.inputport import UserDeleterIF


class UserDeleter(UserDeleterIF):
    logger = logging.getLogger("app")

    def __init__(self, repo: UserRepository) -> None:
        self.repo = repo

    def DeleteUser(self, user_id: int):
        '''ユーザーを削除するビジネスロジック

        Args:
            user_id (int): ユーザーID
        '''
        self.logger.info("execute a delete operation",
                         extra={"details": {"user_id": user_id}})
        self.repo.delete(user_id)

    def DeleteUsers(self, user_ids: List[int]):
        '''ユーザーを一括削除するビジネスロジック
            Repositoryがdelete関数でN件削除をサポートしている。
            そのためDeleteUser関数と同じ実装だが、ビジネスロジックとしては分けておく。
        Args:
            user_ids (List[int]): ユーザーID群
        '''
        self.logger.info("execute delete operations",
                         extra={"details": {"user_id": user_ids}})
        self.repo.delete(user_ids)
