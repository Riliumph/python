
from django.db import models
from rest_framework import serializers
from rest_framework.fields import empty

from base.entity import BaseEntity

# from book_management.books.entity import BookEntity, BookGenreEntity


class GenreEntity(BaseEntity):
    genre_id = models.AutoField(primary_key=True)
    genre_name = models.TextField(null=False)

    class Meta:
        db_table = "genres"


class GenreSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        '''コンストラクタ
        attention:
        スニペット補完を使ってserializers.ModelSerializerのコンストラクタをコピーしてくると正しく動作しなくなる。
        引数の定義を`*args`にして再定義すること。
        '''
        # BookSerializerから参照できるようにインスタンス変数に登録する
        if "read_only" in kwargs.keys():
            self.read_only = kwargs.get("read_only")
        super().__init__(*args, **kwargs)

    class Meta:
        model = GenreEntity
        fields = '__all__'
