
from django.db import models
from rest_framework import serializers

from sample_app.base.entity import BaseEntity

# from sample_app.books.entity import BookEntity, BookGenreEntity


class GenreEntity(BaseEntity):
    genre_id = models.AutoField(primary_key=True)
    genre_name = models.TextField(null=False)

    class Meta:
        db_table = "genres"


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = GenreEntity
        fields = '__all__'
