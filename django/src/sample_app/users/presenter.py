
from typing import Any, Dict

from django.forms.models import model_to_dict

from sample_app.base.outputport import BaseOutputPort
from sample_app.users.entity import UserEntity


class UserPresenter(BaseOutputPort):
    ''' ユーザー情報のレスポンスデータを表現するクラス
    '''

    def __init__(self, entity: UserEntity) -> None:
        self.entity = entity

    def ToJson(self) -> Dict[str, Any]:
        return model_to_dict(self.entity)
