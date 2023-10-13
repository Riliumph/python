import logging
from typing import Any, Dict, List

from django.forms.models import model_to_dict

from sample_app.books.presenter import BookPresenter
from sample_app.books.repository import BookRepository
from sample_app.books.usecase.inputport import *


class BookCreator(BookCreatorIF):
    logger = logging.getLogger("app")

    def __init__(self, repo: BookRepository) -> None:
        self.repo = repo

    def CreateBook(self, data: Dict[str, Any]) -> BookPresenter:
        self.logger.info("execute a create operation",
                         extra={"details": data})
        return BookPresenter(self.repo.create(data))

    def CreateBooks(self, data: List[Dict[str, Any]]) -> List[BookPresenter]:
        self.logger.info("execute create operations",
                         extra={"details": data})
        return BookPresenter(self.repo.create(data))
