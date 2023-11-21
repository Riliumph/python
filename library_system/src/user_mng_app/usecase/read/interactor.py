import logging

from user_mng_app.gateway.repository import UserRepository as UserRepo
from user_mng_app.presenter.presenter import UserPresenter
from user_mng_app.usecase.read import inputport

logger = logging.getLogger("app")


class UserReader(inputport.UserReader):
    def __init__(self, repo: UserRepo):
        self.repo = repo

    def ReadUserById(self, user_id) -> UserPresenter:
        logger.info("execute a read operation",
                    extra={"details": {"user_id": user_id}})
        data = self.repo.get(user_id)
        return UserPresenter(data)
