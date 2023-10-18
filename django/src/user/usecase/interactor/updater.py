import logging
from typing import Any, Dict, List

from django.forms.models import model_to_dict

from user.gateway.user_repository import UserRepository
from user.presenter.user import UserPresenter
from user.usecase.inputport import UserUpdaterIF


class UserUpdater(UserUpdaterIF):
    logger = logging.getLogger("app")

    def __init__(self, repo: UserRepository) -> None:
        self.repo = repo

    def UpdateUser(self, user_id: int, data: Dict[str, Any]) -> UserPresenter:
        '''更新ビジネスロジック

        Args:
            user_id (int): 更新対象のユーザーID
            data (Dict[str, Any]): 更新後のデータ

        Returns:
            Dict[str, Any]: 更新結果
        '''
        self.logger.info("execute update operation",
                         extra={"details": data})
        return UserPresenter(self.repo.update(user_id, data))

    def UpdateUsers(self, user_ids: List[int], data: List[Dict[str, Any]]):
        return super().UpdateUsers(data)
