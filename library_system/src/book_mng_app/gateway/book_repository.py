import logging
from typing import Any, Dict, List

from base.gateway import BaseRepository
from book_mng_app.entity.book import *


class BookRepository(BaseRepository):
    logger = logging.getLogger("app")

    def __init__(self, entity: [BookEntity, BookSerializer]):
        if isinstance(entity, BookEntity):
            self.entity = entity
            self.serializer = None
        elif isinstance(entity, (BookSerializer)):
            self.entity = entity.Meta.model
            self.serializer = entity
        else:
            raise ValueError(f"not support entity type({type(entity)})")

    def get(self,  book_id) -> BookEntity:
        return self.entity.objects.get(book_id=book_id)

    def get_all(self) -> List[BookEntity]:
        return self.entity.objects.all().order_by(self.entity._meta.pk.name)

    def create(self, data: Dict[str, Any]) -> Any:
        '''Entityを新規作成する関数
        Returns:
            int: user_id
        '''
        self.serializer.is_valid(raise_exception=True)
        return self.serializer.save()

    def update(self, user_id, data: Dict[str, Any]) -> None:
        '''Entityを更新する関数
        TODO: user_idなどread_onlyなカラムが更新されるか確認
        '''
        target = self.entity.objects.get(user_id=user_id)
        s = BookSerializer(target, data=data)  # targetが必要なので、依存してしまう
        s.is_valid(raise_exception=True)
        return s.save()

    def delete(self, user_id: int) -> None:
        self.logger.info("repository send user deletion query to DB")
        entity = self.entity.objects.get(user_id=user_id)
        entity.delete()
        self.logger.info("user was deleted",
                         extra={"details": {"user_id": user_id}})
