from django.db import models
from rest_framework import serializers

TABLE_NAME = "users"


class UserModel(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = TABLE_NAME


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = '__all__'
