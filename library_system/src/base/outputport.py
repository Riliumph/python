import abc
from typing import Any, Dict

from base.entity import BaseEntity


class BaseOutputPort(abc.ABC):
    @abc.abstractmethod
    def __init__(self, entity: BaseEntity) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def ToJson(self) -> Dict[str, Any]:
        ''' EntityをDict(Json)形式に変換するメソッド
            Go言語のechoフレームワークはHTTP STATUSまで変換するが、
            今回は、Entityだけに限定することとする。
        Returns:
            Dict[str, Any]: Entity
        '''

        raise NotImplementedError()
