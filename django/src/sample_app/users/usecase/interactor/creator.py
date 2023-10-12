import logging
from typing import Any, Dict, List

from django.forms.models import model_to_dict

from sample_app.users.repository import UserRepository
from sample_app.users.usecase.inputport import UserCreatorIF


class UserCreator(UserCreatorIF):
    logger = logging.getLogger("app")

    def __init__(self, repo: UserRepository) -> None:
        self.repo = repo

    def CreateUser(self, data: Dict[str, Any]) -> Dict[str, Any]:
        self.logger.info("execute create operation",
                         extra={"details": data})
        response = self.repo.create(data)
        return model_to_dict(response)

    def CreateUsers(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return super().CreateUsers(data)
