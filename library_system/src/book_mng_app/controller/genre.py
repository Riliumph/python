'''ジャンル情報のAPIを記述したモジュール
ジャンルの一覧・登録・更新・削除を定義している。
可能な限りDjangoの機能を用いて最小限のコードでの実現を目指す。
'''

import logging

from rest_framework.exceptions import *
from rest_framework.generics import *
from rest_framework.request import Request
from rest_framework.response import Response

from book_mng_app.entity.genre import GenreEntity, GenreSerializer

logger = logging.getLogger("app")


class ListCreate(ListCreateAPIView):
    '''本のジャンルの全取得・作成API
    バルク処理未対応
    '''

    lookup_field = GenreEntity._meta.pk.name
    queryset = GenreEntity.objects.all()
    serializer_class = GenreSerializer


class GetUpdateDestroy(RetrieveUpdateDestroyAPIView):
    '''本のジャンルの取得・更新・削除API
    バルク処理未対応
    '''
    lookup_field = GenreEntity._meta.pk.name
    queryset = GenreEntity.objects.all()
    serializer_class = GenreSerializer
