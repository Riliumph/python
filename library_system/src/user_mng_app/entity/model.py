from django.db import models

from base.entity import BaseEntity

TABLE_NAME = "users"


class User(BaseEntity):
    # PostgreSQL15の限界制度
    digit_before_dec_pt = 131072
    digit_after_dec_pt = 16383
    user_id = models.AutoField(primary_key=True)
    user_name = models.TextField(null=False)
    age = models.IntegerField(null=False)
    wage = models.DecimalField(max_digits=digit_before_dec_pt+2,
                               decimal_places=2)
    enrollment_day = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = TABLE_NAME
