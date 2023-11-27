import logging

from django.db import models
from rest_framework import serializers

from base.entity import BaseEntity
from book_mng_app.entity.book import BookSerializer

logger = logging.getLogger("app")


class GenreEntity(BaseEntity):
    '''genresテーブルを表現するモデルクラス
    DBのテーブルにおいて、books - books_genres - genresの関係性を持つ。
    '''
    genre_id = models.AutoField(primary_key=True)
    genre_name = models.TextField(null=False)

    class Meta:
        db_table = "genres"


class GenreSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        '''コンストラクタ
        他のシリアライザ（主にBookSerializer）から参照されることを想定した処理が実装済み
        詳細は、BookSerializer#update()を参照
        Args:
            kwargs["read_only"]: 他シリアライザから参照される際のエラー回避用フラグ
        '''
        if BookSerializer.ro_flag_name in kwargs.keys():
            logger.info("called from other serializer")
            self.read_only = kwargs.get(BookSerializer.ro_flag_name)
        super().__init__(*args, **kwargs)

    class Meta:
        model = GenreEntity
        fields = '__all__'
