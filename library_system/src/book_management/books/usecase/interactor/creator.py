import logging
from typing import Any, Dict, List

from django.forms.models import model_to_dict

from book_management.books.presenter import BookPresenter
from book_management.books.repository import BookRepository
from book_management.books.usecase.inputport import *


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
