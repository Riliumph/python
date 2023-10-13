from django.db import models
from rest_framework import serializers

from sample_app.base.entity import BaseEntity
from sample_app.books_genres.entity import BookGenreEntity
from sample_app.genres.entity import GenreEntity


class BookEntity(BaseEntity):
    book_id = models.AutoField(primary_key=True)
    title = models.TextField(null=False)
    author = models.TextField(null=False)
    publisher = models.TextField(null=False)
    publication_date = models.DateTimeField()
    pages = models.IntegerField(null=False)
    # Book->BookGenre<-Genreの中間テーブルを挟む多対多関係において、
    # BookかGenreのどちらかにManyToManyFieldがあればよい。
    genres = models.ManyToManyField(GenreEntity,
                                    through=BookGenreEntity,
                                    related_name='books')

    class Meta:
        db_table = "books"


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookEntity
        fields = '__all__'
