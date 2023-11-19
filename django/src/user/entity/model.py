from django.db import models

from base.entity import BaseEntity

TABLE_NAME = "users"


class User(BaseEntity):
    user_id = models.AutoField(primary_key=True)
    user_name = models.TextField(null=False)

    class Meta:
        db_table = TABLE_NAME
