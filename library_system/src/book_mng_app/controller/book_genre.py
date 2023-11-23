'''本からジャンル情報を引く機能のコントローラモジュール
本管理アプリはDjangoの機能を用いて省コストで実装する。
Djangoのデフォルト機能を使うと最も効率よい。
しかし、books/genresの多対多関係を表現するbooks_genresテーブル全体を見せる機能となってしまう。
本から、その本に紐づけられているジャンル情報のみを制御する処理へオーバーライドする。
'''
import json
import logging

from django.db.utils import IntegrityError
from rest_framework.exceptions import *
from rest_framework.generics import *
from rest_framework.request import Request
from rest_framework.response import Response

from book_mng_app.entity.book import *
from book_mng_app.entity.genre import *

logger = logging.getLogger("app")


class ListCreate(ListCreateAPIView):
    '''本に付属するジャンル情報を一覧・付与を行うAPI
    '''
    # Browsable API Rendererの作るUIが基準にする情報
    # Serializerの中の見て、以下のように処理が変化する模様。
    # - book_idがInteger型なら<input type="number">な入力フィールドを構築
    # - book_nameがText型ならtext areaな入力フィールドを構築
    # - book_idがForeignKey型なら選択型のプルダウンフィールドを構築
    # - etc...
    serializer_class = BookGenreSerializer
    # lookup_field = GenreEntity._meta.pk.name

    def get_queryset(self):
        return BookGenreEntity.objects.all()

    def get_serializer(self, *args, **kwargs):
        return super().get_serializer(*args, **kwargs)

    def get(self, request, book_id, *args, **kwargs):
        '''本に付与されているジャンル情報を一覧取得するAPI
        デフォルトの実装だとbooks_genres多対多テーブルをすべて取得してしまうので実装する
        '''

        data = None
        try:
            # GenreEntityにはBookEntity側でManyToManyを張ってるのでbooksテーブルを参照できる。
            # related_name='books'なので、related_name__pkがbooks__book_idとなる
            genres = GenreEntity.objects.filter(books__book_id=book_id)
            serializer = GenreSerializer(genres, many=True)
            data = serializer.data
        except GenreEntity.DoesNotExist as e:
            logger.error("not error")
            raise NotFound
        except Exception as e:
            logger.error(e)
            raise APIException
        return Response(status=200, data=data)

    def post(self, request, *args, **kwargs):
        '''本にジャンル情報を付与するAPI
        デフォルトのままだと、serializerをGenreSerializerにしているのでジャンルテーブルに追加の処理となる。
        TODO:
        既存のジャンル情報を取得して、それを付与する形にしないといけない。
        '''
        return super().post(request, *args, **kwargs)


class GetUpdateDestroy(RetrieveUpdateDestroyAPIView):
    '''BookからGenreを取得・修正・削除するためのAPI
    Genre自体の取得・修正・削除ではなく、Bookへ付与する物である。
    '''
    serializer_class = GenreSerializer
    lookup_field = GenreEntity._meta.pk.name

    def get_queryset(self):
        return GenreEntity.objects.all().order_by(self.lookup_field)

    def get(self, request, book_id, genre_id, *args, **kwargs):
        presenter = None
        data = None
        try:
            # GenreEntityにはBookEntity側でManyToManyを張ってるのでbooksテーブルを参照できる。
            genres = GenreEntity.objects.filter(books__book_id=book_id)
            logger.info(genres)
            logger.info(f"{type(genres)}")
            serializer = GenreSerializer(genres, many=True)
            data = serializer.data
            logger.info(data)
            logger.info(f"{type(data)}")
        except GenreEntity.DoesNotExist as e:
            logger.error("not error")
            raise NotFound
        except Exception as e:
            logger.error(e)
            raise APIException
        return Response(status=200, data=data)
