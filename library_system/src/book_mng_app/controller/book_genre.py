import json
import logging

from django.forms.models import model_to_dict
from rest_framework.exceptions import *
from rest_framework.generics import *
from rest_framework.request import Request
from rest_framework.response import Response

from book_mng_app.entity.book import *
from book_mng_app.entity.genre import *

logger = logging.getLogger("app")


class ListCreate(ListCreateAPIView):
    '''本に付属するジャンル情報を取得・付与を行うAPI
    基本的にこのAPIをこのページ構成で使うことはあり得ない。
    通常は、books/{id}/genresなど、本をたどって編集する。
    ただし、将来、管理者用のバルク処理としてこのURLが使われる可能性は否定しないので一応実装してみた。
    '''
    serializer_class = BookGenreSerializer

    def get_queryset(self):
        return BookGenreEntity.objects.all()


class GetUpdateDestroy(RetrieveUpdateDestroyAPIView):
    '''BookからGenreを取得・修正・削除するためのAPI
    Genre自体の取得・修正・削除ではなく、Bookへ付与する物である。
    TODO: 付与できないからRetrieveUpdateDestroyAPIViewではない可能性が高い
    books_genresの多対多テーブルを

    Args:
        RetrieveUpdateDestroyAPIView (_type_): _description_

    Raises:
        NotFound: _description_
        NotFound: _description_
        APIException: _description_

    Returns:
        _type_: _description_
    '''
    serializer_class = GenreSerializer
    lookup_field = GenreEntity._meta.pk.name

    def get_queryset(self):
        return GenreEntity.objects.all().order_by(self.lookup_field)

    def get(self, request, book_id, *args, **kwargs):
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
