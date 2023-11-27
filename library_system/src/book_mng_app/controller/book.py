'''本のAPIを記述したモジュール
本の一覧・登録・更新・削除を定義している。
可能な限りDjangoの機能を用いて最小限のコードでの実現を目指す。
'''
import logging

from rest_framework.generics import *

from book_mng_app.entity.book import *

logger = logging.getLogger("app")


class ListCreate(ListCreateAPIView):
    '''本の全取得・作成API
    '''
    lookup_field = BookEntity._meta.pk.name
    queryset = BookEntity.objects.all()
    # Browsable API Rendererの作るUIが基準にする情報
    # Serializerの中の見て、以下のように処理が変化する模様。
    # - book_idがInteger型なら<input type="number">な入力フィールドを構築
    # - book_nameがText型ならtext areaな入力フィールドを構築
    # - book_idがForeignKey型なら選択型のプルダウンフィールドを構築
    # - etc...
    serializer_class = BookSerializer

    def get_serializer(self, *args, **kwargs):
        '''serializerの取得関数
        serializer_classをコンストラクトする関数。
        serializer仕様は、manyキーの有無でListSerializerを代用するように実装されている。
        Bookにはbulk処理のためにListSerializerに対応している。

        Returns:
            BookSerializer: 単一データ用のシリアライザ
            BookListSerializer: 複数データ用のシリアライザ
        '''
        # []ではkeyError例外が発生するため、例外発生しないget()を使う
        if isinstance(kwargs.get('data'), list):
            logger.info("detected bulk data")
            logger.info("set up flag for List Serializer")
            kwargs['many'] = True
        return super().get_serializer(*args, **kwargs)


class GetUpdateDestroy(RetrieveUpdateDestroyAPIView):
    '''本の取得・更新・削除API
    '''
    lookup_field = BookEntity._meta.pk.name
    queryset = BookEntity.objects.all()
    serializer_class = BookSerializer
