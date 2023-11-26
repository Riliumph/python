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
        serializer_classをBookGenreSerializerにしているのでBrowsable API Rendererは外部キーの選択UIを構築する。
        URLの設計上はパスパラメータに対するbook_idに対して処理を行うが、無意味にbook_idを選択するUIが構築されている。
        現状、これを回避する手段は調べても見つからなかった。
        '''
        data = None
        try:
            req_body = json.loads(request.body.decode("utf-8"))
            req_body["book_id"] = kwargs["book_id"]  # bodyのbook_idは信用しない
            serializer = self.get_serializer(data=req_body)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            self.perform_create()
        except IntegrityError as e:
            # 既に重複している場合、UNIQUE制約で弾かれてしまう
            # IntegrityError at /api/v1/books/1/genres
            # duplicate key value violates unique constraint "books_genres_book_id_genre_id_key"
            # DETAIL:  Key (book_id, genre_id)=(2, 1) already exists.
            logger.warn(f"already exist: {e}", exc_info=e)
            # 重複なので200 OKを返しても409 Conflictを返しても良い気がする
            # return Response(status=409)
            raise APIException
        return super().post(request, *args, **kwargs)


class GetDestroy(RetrieveDestroyAPIView):
    '''Bookに付与されているGenreを取得・削除するためのAPI
    Genre自体への操作取得・削除ではなく、Bookへ付与する物である。
    '''
    serializer_class = BookGenreSerializer
    lookup_field = GenreEntity._meta.pk.name

    def get_queryset(self):
        return GenreEntity.objects.all().order_by(self.lookup_field)

    def get(self, request, book_id, genre_id, *args, **kwargs):
        data = None
        try:
            # GenreEntityにはBookEntity側でManyToManyを張ってるのでbooksテーブルを参照できる。
            genres = GenreEntity.objects.filter(books__book_id=book_id,
                                                genre_id=genre_id)
            serializer = GenreSerializer(genres, many=True)
            data = serializer.data
        except GenreEntity.DoesNotExist as e:
            logger.error("not error")
            raise NotFound
        except Exception as e:
            logger.error(e)
            raise APIException
        return Response(status=200, data=data)
