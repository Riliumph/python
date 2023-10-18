import logging
from typing import Any, Dict, List, Union

from django.db.models import Q

from sample_app.base.repository import BaseRepository
from user.entity.user import *

logger = logging.getLogger("app")


class UserRepository(BaseRepository):

    def __init__(self, entity: [UserEntity, UserSerializer]):
        if isinstance(entity, UserEntity):
            self.entity = entity
            self.serializer = None
        elif isinstance(entity, (UserSerializer, UserListSerializer)):
            self.entity = entity.Meta.model
            self.serializer = entity
        else:
            raise ValueError(f"not support entity type({type(entity)})")

    def get(self,  user_id) -> UserEntity:
        return self.entity.objects.get(user_id=user_id)

    def all(self) -> List[UserEntity]:
        return self.entity.objects.all().order_by(self.entity._meta.pk.name)

    def create(self, data: Dict[str, Any]) -> List[UserEntity]:
        '''Entityを新規作成する関数
        ListSerializerでコンストラクトすることで複数データを一括作成することが可能。
        ListSerializerにはbulk_createを用いて一括作成をサポートしたcreate関数が定義されている必要がある。

        Returns:
            List[UserEntity]: _description_
        '''
        self.serializer.is_valid(raise_exception=True)
        created_info = self.serializer.save()
        return created_info

    def update(self, user_id, data: Dict[str, Any]) -> None:
        '''Entityを更新する関数
        TODO: user_idなどread_onlyなカラムが更新されるか確認
        '''
        target = self.entity.objects.get(user_id=user_id)
        s = UserSerializer(target, data=data)
        s.is_valid(raise_exception=True)
        return s.save()

    def delete(self, user_ids: Union[int, List[int]]):
        '''Entityを削除する関数
           PythonではOverload機能がないため、複数を前提に実装する。

        Args:
            user_ids (Union[int, List[int]]): ユーザーID
        '''
        logger.info("repository send user deletion query to DB")
        or_condition = Q()
        for user_id in user_ids:
            or_condition |= Q(user_id=user_id)
        deleted_info = self.entity.objects.filter(or_condition).delete()
        # return deleted count & type as tuple
        logger.debug(f"{deleted_info}")
        logger.info("user was deleted",
                    extra={"details": {"user_id": user_ids}})
