import json
import logging

from django.forms.models import model_to_dict
from rest_framework.exceptions import *
from rest_framework.generics import *
from rest_framework.request import Request
from rest_framework.response import Response

from book_management.books.entity import BookEntity, BookSerializer
from book_management.books.repository import BookRepository
from book_management.genres.entity import GenreEntity, GenreSerializer

logger = logging.getLogger("app")


class GetUpdateDestroy(RetrieveUpdateDestroyAPIView):
    '''本の取得・更新・削除API
    Djangoの機能をフルに活用して最小コードで書いてみる
    '''
    serializer_class = BookSerializer
    lookup_field = BookEntity._meta.pk.name

    def get_queryset(self):
        return BookEntity.objects.all().order_by(self.lookup_field)


class GetAllCreate(ListCreateAPIView):
    '''本の全取得・作成API
    Djangoの機能をフルに活用して最小コードで書いてみる
    '''
    serializer_class = BookSerializer
    lookup_field = BookEntity._meta.pk.name

    def get_queryset(self):
        return BookEntity.objects.all().order_by(self.lookup_field)

    def get_serializer(self, *args, **kwargs):
        # []ではkeyError例外が発生するため、例外発生しないget()を使う
        if isinstance(kwargs.get('data'), list):
            kwargs['many'] = True
        return super().get_serializer(*args, **kwargs)

    def get(self, request: Request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class BookGenreGetAllCreate(ListCreateAPIView):
    '''本に付属するジャンル情報を取得・付与を行うAPI
    '''
    serializer_class = BookSerializer
    lookup_field = BookEntity._meta.pk.name

    def get_queryset(self):
        return GenreEntity.objects.all().order_by(self.lookup_field)

    def get(self, request, book_id, *args, **kwargs):
        res = {}
        try:
            logger.info("show variable", extra={
                        "details": kwargs, "book_id": book_id})
            res = model_to_dict(BookEntity.objects.get(book_id=book_id))
        except APIException as e:
            logger.error("rest_framework exception", extra={
                         "exception": e.get_full_details()}, exc_info=True)
            raise e  # rethrow
        except Exception as e:
            logger.error(f"unexpected exception",
                         exc_info=True, stack_info=True)
            raise APIException  # translate unexpected exception into 500
        return Response(status=200, data=res)

    def post(self, request, book_id, *args, **kwargs):
        # 引数チェックのみ
        try:
            logger.info(type(request))
            req_body = json.loads(request.body.decode("utf-8"))
            logger.info("show variable", extra={"details": {
                        "book_id": book_id, "body": req_body}})
        except APIException as e:
            logger.error("rest_framework exception", extra={
                         "exception": e.get_full_details()}, exc_info=True)
            raise e  # rethrow
        except Exception as e:
            logger.error(f"unexpected exception",
                         exc_info=True, stack_info=True)
            raise APIException  # translate unexpected exception into 500
        return Response(status=201)