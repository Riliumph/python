import logging
from typing import Any, Dict, List

from base.presenter import BasePresenter
from book_management.gateway.book_repository import BookRepository
from book_management.usecase.inputport import *


class BookCreator(BookCreatorIF):
    logger = logging.getLogger("app")

    def __init__(self, repo: BookRepository) -> None:
        self.repo = repo

    def CreateBook(self, data: Dict[str, Any]) -> BasePresenter:
        self.logger.info("execute a create operation",
                         extra={"details": data})
        return BasePresenter(self.repo.create(data))

    def CreateBooks(self, data: List[Dict[str, Any]]) -> List[BasePresenter]:
        self.logger.info("execute create operations",
                         extra={"details": data})
        return BasePresenter(self.repo.create(data))
