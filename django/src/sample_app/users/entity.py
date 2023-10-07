from django.db import models
from rest_framework import serializers

from sample_app.base.entity import BaseEntity

TABLE_NAME = "users"


class UserEntity(BaseEntity):
    user_id = models.AutoField(primary_key=True)
    user_name = models.TextField(null=False)

    class Meta:
        db_table = TABLE_NAME


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserEntity
        fields = '__all__'
