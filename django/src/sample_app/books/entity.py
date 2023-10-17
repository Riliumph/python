import logging
from typing import Any, Dict

from django.db import models
from rest_framework import serializers
from rest_framework.fields import empty

from sample_app.base.entity import BaseEntity
from sample_app.books_genres.entity import BookGenreEntity, BookGenreSerializer
from sample_app.genres.entity import GenreEntity, GenreSerializer

logger = logging.getLogger("app")


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
    '''BookEntityのシリアライザ

    Class Attributes:
        genres (GenreSerializer): 多対多関係のGenreEntityを、BookEntityと同時に参照する際に使用されるシリアライザ

    Returns:
        _type_: _description_
    '''
    # Model側でManyToManyFieldを使っている場合、多対多先のモデル（テーブル）をどの程度参照するかによって実装が異なる。
    # Bookにおいては、Book - BookGenre - Genreの関係性を持つ。
    # BookからGenreを参照する際に、ID（genre_id）までの参照で良ければ、GenreSerializerを使う必要はない。
    # Genreの内容まで参照したい場合は、model側の変数名と同じ名前でGenreSerializerを使う必要がある。
    genres = GenreSerializer(many=True, read_only=True)

    def update(self, instance: BookEntity, validated_data: Dict[str, Any]) -> BookEntity:
        '''BookEntityの更新処理の特殊化
        Bookの更新APIから多対多関係のGenreを更新することはできない。
        更新する場合、Serializer#update()を実装して対応しろと出てくるので、あくまで実験的な試みとしてやってみる。
        read_only=Noneを設定することで、独自のupdateが実行されてAssertion例外が送出される。
        read_only=True/Falseでは、通常のDjangoと同じ挙動を取る。
        Args:
            instance (BookEntity): 更新対象の本情報
            validated_data (Dict[str, Any]): 更新後の本情報

        Returns:
            BookEntity: 正常に更新された本情報
        '''
        # BookSerializer#update()が実装されていない場合の挙動と同じ
        if self.fields["genres"].read_only is not None:
            # True設定の場合、正しく動作
            # False設定の場合、Assertion例外（The `.update()` method does not support writable nested fields by default.）
            return super().update(instance, validated_data)

        # Noneを指定して明示的に独自update()を実行する場合
        instance.title = validated_data.get('title', instance.title)
        instance.author = validated_data.get('author', instance.author)
        instance.publisher = validated_data.get('publisher',
                                                instance.publisher)
        instance.publication_date = validated_data.get('publication_date',
                                                       instance.publication_date)
        instance.save()
        # この本のジャンル情報を取得する
        books_genres = BookGenreEntity.objects.filter(book_id=instance.book_id)
        # Getの際にBookSerializer#genresが使われたので、UPDATEで使うかというと使えない。
        # BookGenreのモデルを修正する必要があるため、GenreSerializerでは不十分である。
        # しかし、ここでBookGenreSerializerを使うのもまたいくつかの問題を抱える。
        # ここはBookSerializer#is_validate()が実行された後であり、validated_dataはすべて正常な値であるべきである。
        # しかし、BookSerializerのシリアライズしかされておらず、BookGenreの正常性は評価されていない
        # あと、validated_dataとして飛んでくる情報はBookEntityに該当する物のみである。
        # どうやってupdate()を実装しろというのか。諦める。
        assert False, "BookSerializer#update()でBookGenreEntityを書き換える実装アイデアはない"
        return instance

    class Meta:
        model = BookEntity
        fields = '__all__'
