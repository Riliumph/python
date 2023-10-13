import logging
from typing import Any, Dict, List

from sample_app.base.repository import BaseRepository
from sample_app.books.entity import *


class BookRepository(BaseRepository):
    logger = logging.getLogger("app")

    def __init__(self, entity: BookEntity):
        self.entity = entity

    def get(self,  book_id) -> BookEntity:
        return self.entity.objects.get(book_id=book_id)

    def get_all(self) -> List[BookEntity]:
        return self.entity.objects.all().order_by(self.entity._meta.pk.name)

    def create(self, data: Dict[str, Any]) -> Any:
        '''Entityを新規作成する関数
        Returns:
            int: user_id
        '''
        s = UserSerializer(data=data)
        s.is_valid(raise_exception=True)
        return s.save()

    def update(self, user_id, data: Dict[str, Any]) -> None:
        '''Entityを更新する関数
        TODO: user_idなどread_onlyなカラムが更新されるか確認
        '''
        target = self.entity.objects.get(user_id=user_id)
        s = UserSerializer(target, data=data)
        s.is_valid(raise_exception=True)
        return s.save()

    def delete(self, user_id: int) -> None:
        self.logger.info("repository send user deletion query to DB")
        entity = self.entity.objects.get(user_id=user_id)
        entity.delete()
        self.logger.info("user was deleted",
                         extra={"details": {"user_id": user_id}})
