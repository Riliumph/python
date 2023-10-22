import logging
from typing import Any, Dict, List

from user.gateway import UserRepository as UserRepo
from user.presenter import UserPresenter
from user.usecase.creator import inputport

logger = logging.getLogger("app")


class UserCreator(inputport.UserCreator):
    def __init__(self, repo: UserRepo):
        self.repo = repo

    def CreateUser(self, data: Dict[str, Any]) -> UserPresenter:
        '''ユーザーを作成するビジネスロジック（単一）
        ListSerializerにてbulk_create対応済みだが、ビジネスロジックとしては分けておく。
        ただし、APIはusers#POSTのため、単一専用・複数専用にすることはできない。
        各々を専用のAPIにする場合は、別々のURL#POSTで実装する必要がある。

        Args:
            data (Dict[str, Any]): 登録したいユーザー情報

        Returns:
            UserPresenter: 作成したユーザー情報
        '''
        logger.info("execute a create operation",
                    extra={"details": data})
        return UserPresenter(self.repo.create(data))

    def CreateUsers(self, data: List[Dict[str, Any]]) -> List[UserPresenter]:
        '''ユーザーを作成するビジネスロジック（複数）
        ListSerializerにてbulk_create対応済みだが、ビジネスロジックとしては分けておく。
        ただし、APIはusers#POSTのため、単一専用・複数専用にすることはできない。
        各々を専用のAPIにする場合は、別々のURL#POSTで実装する必要がある。

        Args:
            data (List[Dict[str, Any]]): 登録したいユーザー情報群

        Returns:
            List[UserPresenter]: 作成したユーザー情報群
        '''
        logger.info("execute create operations",
                    extra={"details": data})
        return UserPresenter(self.repo.create(data))
