import logging
from typing import List, Dict, Any

from django.forms.models import model_to_dict

from sample_app.users.usecase.inputport import UserUpdaterIF
from sample_app.users.repository import UserRepository
from sample_app.users.entity import UserEntity, UserSerializer


class UserUpdater(UserUpdaterIF):
    logger = logging.getLogger("app")

    def __init__(self, repo: UserRepository) -> None:
        self.repo = repo

    def UpdateUser(self, user_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        '''更新ビジネスロジック

        Args:
            user_id (int): 更新対象のユーザーID
            data (Dict[str, Any]): 更新後のデータ

        Returns:
            Dict[str, Any]: 更新結果
        '''
        self.logger.info("execute update operation",
                         extra={"details": data})
        response = self.repo.update(user_id, data)
        return model_to_dict(response)

    def UpdateUsers(self, user_ids: List[int], data: List[Dict[str, Any]]):
        return super().UpdateUsers(data)
