from django.db import models
from rest_framework import serializers

from sample_app.base.entity import BaseEntity
from sample_app.books_genres.entity import BookGenreEntity
from sample_app.genres.entity import GenreEntity, GenreSerializer


class BookEntity(BaseEntity):
    '''bookテーブルを表現するモデルクラス
    DBのテーブルにおいて、books - books_genres - genresの関係性を持つ。
    '''
    book_id = models.AutoField(primary_key=True)
    title = models.TextField(null=False)
    author = models.TextField(null=False)
    publisher = models.TextField(null=False)
    publication_date = models.DateTimeField()
    pages = models.IntegerField(null=False)
    # Book->BookGenre<-Genreの中間テーブルを挟む多対多関係において、BookかGenreのどちらかにManyToManyFieldがあればよい。
    genres = models.ManyToManyField(GenreEntity,
                                    through=BookGenreEntity,
                                    related_name='books')

    class Meta:
        db_table = "books"


class BookSerializer(serializers.ModelSerializer):
    # Model側でManyToManyFieldを使っている場合、多対多先のモデル（テーブル）をどの程度参照するかによって実装が異なる。
    # Bookにおいては、Book - BookGenre - Genreの関係性を持つ。
    # BookからGenreを参照する際に、ID（genre_id）までの参照で良ければ、GenreSerializerを使う必要はない。
    # Genreの内容まで参照したい場合は、model側の変数名と同じ名前でGenreSerializerを使う必要がある。
    genres = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = BookEntity
        fields = '__all__'
