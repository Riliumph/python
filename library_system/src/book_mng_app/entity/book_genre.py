from typing import Any, Dict, List

from django.db import models
from rest_framework import serializers

from base.entity import BaseEntity

# Book->BookGenre<-Genreの多対多関係を構築する時に遅延評価するため必要ない
# from book_mng_app.books.entity import BookEntity
# from book_mng_app.genres.entity import GenreEntity


class BookGenreEntity(BaseEntity):
    '''books_genresテーブルの1レコードを表現するモデルクラス
    多対多テーブルとして特殊な実装が施されている。
    '''
    id = models.AutoField(primary_key=True)
    # BookはBookGenreに依存しBookGenreもBook（とGenre）に依存するため、
    # どちらかで遅延評価しないと循環参照が発生する。
    # 外部キーはxx_idがDjangoの命名規則なので、genre_id_idになることを回避するためカラム指定する
    book_id = models.ForeignKey('BookEntity',
                                db_column="book_id",
                                on_delete=models.CASCADE)
    genre_id = models.ForeignKey('GenreEntity',
                                 db_column="genre_id",
                                 on_delete=models.CASCADE)

    class Meta:
        db_table = "books_genres"


class BookGenreListSerializer(serializers.ListSerializer):
    '''複数処理用のシリアライザクラス
    '''

    def create(self, validated_data: List[Dict[str, Any]]) -> List[BookGenreEntity]:
        '''DBへの登録処理関数
        Args:
            validated_data (List[Dict[str, Any]]): 登録したいデータ

        Returns:
            List[BookGenreEntity]: 登録後のデータ
        '''
        data = [BookGenreEntity(**vd) for vd in validated_data]
        return BookGenreEntity.objects.bulk_create(data)

    class Meta:
        model = BookGenreEntity
        fields = '__all__'


class BookGenreSerializer(serializers.ModelSerializer):
    '''単一処理用のシリアライザクラス
    '''
    class Meta:
        model = BookGenreEntity
        fields = '__all__'
        list_serializer_class = BookGenreListSerializer  # バルク処理用のListSerializer
