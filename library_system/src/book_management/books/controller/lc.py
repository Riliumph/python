import logging

from rest_framework.generics import *

from book_management.books.entity.entity import *

logger = logging.getLogger("app")


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
