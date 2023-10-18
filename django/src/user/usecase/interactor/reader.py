import logging

from user.gateway.user_repository import UserRepository
from user.presenter.user import UserPresenter
from user.usecase.inputport import UserReaderIF


class UserReader(UserReaderIF):
    logger = logging.getLogger("app")

    def __init__(self, repo: UserRepository):
        self.repo = repo

    def ReadUserById(self, user_id) -> UserPresenter:
        self.logger.info("execute delete operation",
                         extra={"details": {"user_id": user_id}})
        data = self.repo.get(user_id)
        return UserPresenter(data)
