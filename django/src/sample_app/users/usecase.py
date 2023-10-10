import logging
from typing import Any, Dict

from sample_app.base.usecase import BaseInputPort
from sample_app.users.repository import UserRepository


class UserCreateInteractor(BaseInputPort):
    logger = logging.getLogger("app")

    def __init__(self, repo: UserRepository) -> None:
        self.repo = repo

    def __call__(self, request: Dict[str, Any]) -> Dict[str, Any]:
        self.logger.info("interactor execute create operation",
                         extra={"details": request})
        response = self.repo.create(request)
        return response


class UserUpdateInteractor(BaseInputPort):
    logger = logging.getLogger("app")

    def __init__(self, repo: UserRepository) -> None:
        self.repo = repo

    def __call__(self, request: Dict[str, Any]) -> Dict[str, Any]:
        self.logger.info("interactor execute update operation",
                         extra={"details": request})
        self.repo.update(request)
        return None


class UserDeleteInteractor(BaseInputPort):
    logger = logging.getLogger("app")

    def __init__(self, repo: UserRepository) -> None:
        self.repo = repo

    def __call__(self, request: Dict[str, Any]) -> Dict[str, Any]:
        self.logger.info("interactor send delete operation",
                         extra={"details": request})
        user_id = request["user_id"]
        self.repo.delete(user_id)
        return None
