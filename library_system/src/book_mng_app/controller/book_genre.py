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


class BookGenreListCreate(ListCreateAPIView):
    '''本に付属するジャンル情報を取得・付与を行うAPI
    '''
    serializer_class = BookSerializer
    lookup_field = BookEntity._meta.pk.name

    def get_queryset(self):
        return GenreEntity.objects.all().order_by(self.lookup_field)

    def get(self, request: Request, book_id, *args, **kwargs):
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

    def post(self, request: Request, book_id, *args, **kwargs):
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
