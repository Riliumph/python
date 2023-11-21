import logging

from rest_framework.exceptions import *
from rest_framework.generics import *
from rest_framework.request import Request
from rest_framework.response import Response

from book_management.genres.entity import GenreEntity, GenreSerializer

logger = logging.getLogger("app")


class GetUpdateDestroy(RetrieveUpdateDestroyAPIView):
    '''本のジャンルの取得・更新・削除API
    Djangoの機能をフルに活用して最小コードで書いてみる
    '''
    serializer_class = GenreSerializer
    lookup_field = GenreEntity._meta.pk.name

    def get_queryset(self):
        return GenreEntity.objects.all().order_by(self.lookup_field)


class GetAllCreate(ListCreateAPIView):
    '''本のジャンルの全取得・作成API
    Djangoの機能をフルに活用して最小コードで書いてみる
    '''
    serializer_class = GenreSerializer
    lookup_field = GenreEntity._meta.pk.name

    def get_queryset(self):
        return GenreEntity.objects.all().order_by(self.lookup_field)
