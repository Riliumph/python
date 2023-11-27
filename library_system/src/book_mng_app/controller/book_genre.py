'''本からジャンル情報を引く機能のモジュール
本管理アプリはDjangoの機能を用いて省コストで実装する。
Djangoのデフォルト機能を使うと最も効率よい。
しかし、books/genresの多対多関係を表現するbooks_genresテーブル全体を見せる機能となってしまう。
本から、その本に紐づけられているジャンル情報のみを制御する処理へオーバーライドする。
'''
import json
import logging

from django.db.utils import IntegrityError
from rest_framework import exceptions as drf_exc
from rest_framework.generics import *
from rest_framework.request import Request
from rest_framework.response import Response

from book_mng_app.entity.book import *
from book_mng_app.entity.book_genre import *
from book_mng_app.entity.genre import *

logger = logging.getLogger("app")


class ListCreate(ListCreateAPIView):
    '''本に付属するジャンル情報を一覧・付与を行うAPI
    '''
    queryset = BookGenreEntity.objects.all()
    serializer_class = BookGenreSerializer

    def get(self, request, book_id, *args, **kwargs):
        '''本に付与されているジャンル情報を一覧取得するAPI
        デフォルトの実装だとbooks_genres多対多テーブルをすべて取得してしまうので実装する
        '''
        try:
            # GenreEntityにはBookEntity側でManyToManyを張ってるのでbooksテーブルを参照できる。
            # 参照方法は`related_name__pk`の形。
            # - related_nameは、ManyToMany定義で採用したrelated_name(books)
            # - pkは、Model._meta.pk.name(book_id)
            genres = GenreEntity.objects.filter(books__book_id=book_id)
            serializer = GenreSerializer(genres, many=True)
            return Response(status=200, data=serializer.data)
        except GenreEntity.DoesNotExist as e:
            logger.error("not found", extra={"book_id": book_id})
            raise drf_exc.NotFound
        except Exception as e:
            logger.error(e)
            raise drf_exc.APIException

    def post(self, request, book_id, *args, **kwargs):
        '''本にジャンル情報を付与するAPI
        serializer_classをBookGenreSerializerにしているのでBrowsable API Rendererは外部キーの選択UIを構築する。
        URLの設計上はパスパラメータに対するbook_idに対して処理を行うが、無意味にbook_idを選択するUIが構築されている。
        現状、これを回避する手段は調べても見つからなかった。
        '''
        try:
            data = request.data.copy()  # to mutable
            data["book_id"] = book_id  # bodyのbook_idは信用しない
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(status=200, data=serializer.data)
        except IntegrityError as e:
            # 重複したデータは、UNIQUE制約で弾かれてしまう
            # IntegrityError at /api/v1/books/1/genres
            # duplicate key value violates unique constraint "books_genres_book_id_genre_id_key"
            # DETAIL:  Key (book_id, genre_id)=(2, 1) already exists.
            logger.warn(f"already exist: {e}", exc_info=e)
            # 重複なので200 OKを返しても409 Conflictを返しても良い気がする
            return Response(status=409)
        except json.decoder.JSONDecodeError as e:
            logger.error(f"{e}", exc_info=e, stack_info=True)
            raise drf_exc.ValidationError(f"{e}")
        except Exception as e:
            logger.error(f"{e}", exc_info=e, stack_info=True)
            raise drf_exc.APIException


class GetDestroy(RetrieveDestroyAPIView):
    '''Bookに付与されているGenreを取得・削除するためのAPI
    Genre自体への操作取得・削除ではなく、Bookへ付与する物である。
    '''
    serializer_class = BookGenreSerializer
    queryset = BookGenreEntity.objects.all()

    def get(self, request, book_id, genre_id, *args, **kwargs):
        data = None
        try:
            # GenreEntityにはBookEntity側でManyToManyを張ってるのでbooksテーブルを参照できる。
            genres = GenreEntity.objects.filter(books__book_id=book_id,
                                                genre_id=genre_id)
            serializer = GenreSerializer(genres, many=True)
            return Response(status=200, data=serializer.data)
        except GenreEntity.DoesNotExist as e:
            logger.error("not found", extra={"book_id": book_id,
                                             "genre_id": genre_id})
            raise drf_exc.NotFound
        except Exception as e:
            logger.error(f"{e}", exc_info=e, stack_info=True)
            raise drf_exc.APIException

    def delete(self, request, book_id, genre_id, *args, **kwargs):
        '''Bookに付与されているGenre情報を剥奪するAPI
        デフォルトは、`GenericAPIView::get_object()`が`lookup_field`もしくは`lookup_url_kwarg`に設定されたカラム名を使って、受信した辞書データとDBを突合して対象のデータを特定する。
        本来は、1つのデータでレコードを特定するPK情がリクエストされる想定である。
        今回の対象はbookとgenreを多対多で紐づけるbooks_genesテーブルである。
        SQLアンチパターンにもあるが、多対多テーブルにおけるPKは基本的に無意味である。
        その本質はbook_idとgenre_idのUNIQUE制約がPKの役割を果たしている。
        しかし、DjangoはPKレスなテーブルを許さないため、無意味なPKを用いている。
        よって、UNIQUEな要素であるbook_idとgenre_idを指定してレコードを物理削除する。
        '''
        try:
            genre = BookGenreEntity.objects.filter(book_id=book_id,
                                                   genre_id=genre_id)
            genre.delete()
        except GenreEntity.DoesNotExist as e:
            logger.error("not found", extra={"book_id": book_id,
                                             "genre_id": genre_id})
            raise drf_exc.NotFound
        except Exception as e:
            logger.error(f"{e}", exc_info=e, stack_info=True)
            raise drf_exc.APIException
        return Response(status=204)  # 物理削除のため204
