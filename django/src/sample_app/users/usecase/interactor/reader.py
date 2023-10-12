import logging
from typing import Any, Dict, List

from django.forms.models import model_to_dict

from sample_app.users.repository import UserRepository
from sample_app.users.usecase.inputport import UserReaderIF


class UserReader(UserReaderIF):
    logger = logging.getLogger("app")

    def __init__(self, repo: UserRepository) -> None:
        self.repo = repo

    def ReadUserById(self, user_id):
        self.logger.info("execute delete operation",
                         extra={"details": {"user_id": user_id}})
        response = self.repo.get(user_id)
        return model_to_dict(response)
