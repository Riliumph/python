from typing import Any, Dict, List

from django.db import models
from rest_framework import serializers

from sample_app.base.entity import BaseEntity

TABLE_NAME = "users"


class User(BaseEntity):
    user_id = models.AutoField(primary_key=True)
    user_name = models.TextField(null=False)

    class Meta:
        db_table = TABLE_NAME


class UserListSerializer(serializers.ListSerializer):
    '''Userの複数対応シリアライザー
    UserSerializerのインスタンス化に際して、「many=True」が指定されるとListSerializerでインスタンス化される。
    '''

    def create(self, validated_data: List[Dict[str, Any]]) -> List[User]:
        '''DBへinsertクエリを送信する関数
        ユーザー情報をトランザクション中に一回のクエリで実行することで高速に作成する。

        Args:
            validated_data (List[Dict[str, Any]]): _description_

        Returns:
            List[UserEntity]: 作成したユーザー情報
        '''
        data = [User(**vd) for vd in validated_data]
        return User.objects.bulk_create(data)

    class Meta:
        model = User
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    '''Userのシリアライザー
    '''
    class Meta:
        model = User
        fields = '__all__'
        list_serializer_class = UserListSerializer
