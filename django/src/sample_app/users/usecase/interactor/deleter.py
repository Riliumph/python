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
        self.logger.info("execute delete operation",
                         extra={"details": {"user_id": user_id}})
        self.repo.delete(user_id)

    def DeleteUsers(self, user_ids: List[int]):
        for user_id in user_ids:
            self.repo.delete(user_id)
