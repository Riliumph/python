import logging

from sample_app.users.presenter import UserPresenter
from sample_app.users.repository import UserRepository
from sample_app.users.usecase.inputport import UserReaderIF


class UserReader(UserReaderIF):
    logger = logging.getLogger("app")

    def __init__(self, repo: UserRepository):
        self.repo = repo

    def ReadUserById(self, user_id) -> UserPresenter:
        self.logger.info("execute delete operation",
                         extra={"details": {"user_id": user_id}})
        data = self.repo.get(user_id)
        return UserPresenter(data)
