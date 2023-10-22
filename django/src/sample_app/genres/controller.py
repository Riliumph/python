import logging

from rest_framework import generics

from sample_app.genres.entity import GenreEntity, GenreSerializer

logger = logging.getLogger("app")


class GetUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    '''本のジャンルの取得・更新・削除API
    Djangoの機能をフルに活用して最小コードで書いてみる
    '''
    serializer_class = GenreSerializer
    lookup_field = GenreEntity._meta.pk.name

    def get_queryset(self):
        return GenreEntity.objects.all().order_by(self.lookup_field)


class GetAllCreate(generics.ListCreateAPIView):
    '''本のジャンルの全取得・作成API
    Djangoの機能をフルに活用して最小コードで書いてみる
    '''
    serializer_class = GenreSerializer
    lookup_field = GenreEntity._meta.pk.name

    def get_queryset(self):
        return GenreEntity.objects.all().order_by(self.lookup_field)
