import logging
from typing import List, Dict, Any


from sample_app.base.repository import BaseRepository

from sample_app.users.entity import UserSerializer
from sample_app.users.entity import UserEntity


class UserRepository(BaseRepository):
    logger = logging.getLogger("app")

    def __init__(self, entity: UserEntity):
        self.entity = entity

    def get(self,  user_id) -> UserEntity:
        return self.entity.objects.get(user_id=user_id)

    def all(self) -> List[UserEntity]:
        return self.entity.objects.all().order_by("user_id")

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
