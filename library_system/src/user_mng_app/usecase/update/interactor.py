import logging
from typing import Any, Dict, List

from base.presenter import BasePresenter
from user_mng_app.gateway.repository import UserRepository as UserRepo
from user_mng_app.usecase.update import inputport

logger = logging.getLogger("app")


class UserUpdater(inputport.UserUpdater):
    def __init__(self, repo: UserRepo):
        self.repo = repo

    def UpdateUser(self, user_id: int, data: Dict[str, Any]) -> BasePresenter:
        '''ユーザーを更新するビジネスロジック

        Args:
            user_id (int): 更新対象のユーザーID
            data (Dict[str, Any]): 更新後のデータ

        Returns:
            Dict[str, Any]: 更新結果
        '''
        logger.info("execute a update operation",
                    extra={"details": data})
        return BasePresenter(self.repo.update(user_id, data))

    def UpdateUsers(self, user_ids: List[int], data: List[Dict[str, Any]]):
        return super().UpdateUsers(data)
