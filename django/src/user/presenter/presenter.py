
from typing import Any, Dict, List, Union

from django.db.models import Model
from django.forms.models import model_to_dict
from rest_framework.utils.serializer_helpers import ReturnDict, ReturnList

from base.outputport import BaseOutputPort
from user.entity.model import User


class UserPresenter(BaseOutputPort):
    ''' ユーザー情報のレスポンスデータを表現するクラス
    '''

    def __init__(self, entity: Union[User, List[User]]) -> None:
        self.entity = entity

    def ToJson(self) -> Union[ReturnDict, ReturnList, Dict[str, Any], List[Dict[str, Any]]]:
        '''出力データをJson形式へ変換する関数
        rest_frameworkのBrowsable API Rendererへ返す場合は、ReturnDictやReturnListが期待される。
        また、curlなどでアクセスしてもrest_frameworkのResponseクラスを使う限りはフロントエンドにはjson返される。
        DRFとしては極力この形で返したい。

        Returns:
            Union[ReturnDict, ReturnList, Dict[str, Any], List[Dict[str, Any]]]: _description_
        '''
        if isinstance(self.entity, (ReturnDict, ReturnList)):
            return self.entity
        if isinstance(self.entity, list):
            if all(isinstance(e, Model) for e in self.entity):
                return [model_to_dict(e) for e in self.entity]
        if isinstance(self.entity, Model):
            return model_to_dict(self.entity)
        return ValueError("presenter not supported data type")
