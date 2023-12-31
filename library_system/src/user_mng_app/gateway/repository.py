import logging
from typing import Any, Dict, List, Union

from django.db.models import Model, Q
from rest_framework.serializers import ListSerializer, ModelSerializer

from base.gateway import BaseRepository
from user_mng_app.entity.model import User
from user_mng_app.entity.validator import *

logger = logging.getLogger("app")


class UserRepository(BaseRepository):
    def __init__(self, entity: [User, UserSerializer]):
        if isinstance(entity, Model):
            self.entity = entity
            self.serializer = None
        elif isinstance(entity, (ModelSerializer, ListSerializer)):
            self.entity = entity.Meta.model
            self.serializer = entity
        else:
            raise ValueError(f"not support entity type({type(entity)})")

    def get(self,  user_id) -> User:
        logger.info("user repository send select query")
        # instanceから検索はできない。クラス定義を使う
        data = self.entity.__class__.objects.get(user_id=user_id)
        serializer = UserSerializer(data)
        return serializer.data

    def all(self) -> List[User]:
        logger.info("user repository send select query")
        data = self.entity.__class__.objects.all().order_by(self.entity._meta.pk.name)
        serializer = UserListSerializer(data)
        logger.info(f"{type(serializer.data)}")
        return serializer.data

    def create(self, data: Dict[str, Any]) -> List[User]:
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
        logger.info("user repository send update query")
        target = self.entity.objects.get(user_id=user_id)
        # 更新対象と更新後データでシリアライザを作り直す必要がある。
        self.serializer = UserSerializer(target, data=data)
        self.serializer.is_valid(raise_exception=True)
        return self.serializer.save()

    def delete(self, user_ids: Union[int, List[int]]):
        '''Entityを削除する関数
           PythonではOverload機能がないため、複数を前提に実装する。

        Args:
            user_ids (Union[int, List[int]]): ユーザーID
        '''
        logger.info("user repository send delete query")
        or_condition = Q()
        for user_id in user_ids:
            or_condition |= Q(user_id=user_id)
        deleted_info = self.entity.objects.filter(or_condition).delete()
        # return deleted count & type as tuple
        logger.debug(f"{deleted_info}")
        logger.info("user was deleted",
                    extra={"details": {"user_id": user_ids}})
