from django.db import models

from base.entity import BaseEntity

TABLE_NAME = "users"


class User(BaseEntity):
    user_id = models.AutoField(primary_key=True)
    user_name = models.TextField(null=False)
    age = models.IntegerField(null=False)
    enrollment_day = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = TABLE_NAME
