import logging

from rest_framework.generics import *

from book_management.books.entity.entity import *

logger = logging.getLogger("app")


class GetUpdateDestroy(RetrieveUpdateDestroyAPIView):
    '''本の取得・更新・削除API
    Djangoの機能をフルに活用して最小コードで書いてみる
    '''
    serializer_class = BookSerializer
    lookup_field = BookEntity._meta.pk.name

    def get_queryset(self):
        return BookEntity.objects.all().order_by(self.lookup_field)
