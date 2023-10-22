
from typing import Any, Dict, List, Union

from django.forms.models import model_to_dict

from sample_app.base.outputport import BaseOutputPort
from user.entity import User


class UserPresenter(BaseOutputPort):
    ''' ユーザー情報のレスポンスデータを表現するクラス
    '''

    def __init__(self, entity: Union[User, List[User]]) -> None:
        self.entity = entity

    def ToJson(self) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        if isinstance(self.entity, list):
            return [model_to_dict(e) for e in self.entity]
        return model_to_dict(self.entity)
