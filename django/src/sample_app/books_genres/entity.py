from django.db import models
from rest_framework import serializers

from sample_app.base.entity import BaseEntity

# Book->BookGenre<-Genreの多対多関係を構築する時に遅延評価するため必要ない
# from sample_app.books.entity import BookEntity
# from sample_app.genres.entity import GenreEntity


class BookGenreEntity(BaseEntity):
    # BookはBookGenreに依存しBookGenreもBook（とGenre）に依存するため、
    # どちらかで遅延評価しないと循環参照が発生する。
    book_id = models.ForeignKey('BookEntity',
                                db_column="book_id",
                                on_delete=models.CASCADE)
    # 外部キーはxx_idがDjangoの命名規則なので、genre_id_idになることを回避するためカラム指定する
    genre_id = models.ForeignKey('GenreEntity',
                                 db_column="genre_id",
                                 on_delete=models.CASCADE)

    class Meta:
        db_table = "books_genres"


class BookGenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookGenreEntity
        fields = '__all__'
