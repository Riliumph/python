import abc
from typing import Any, Dict, List, Union

from base.entity import BaseEntity


class BaseRepository(abc.ABC):
    @abc.abstractmethod
    def __init__(self, model_class: BaseEntity) -> None:
        '''コンストラクタ
        Args:
            entity: Repositoryが用いるEntity
            MockEntityを渡せるように引数で貰う。
            = RepositoryMockは作らないということか
        '''
        raise NotImplementedError()

    @abc.abstractmethod
    def get(self, id: str) -> BaseEntity:
        raise NotImplementedError()

    @abc.abstractmethod
    def all(self) -> List[BaseEntity]:
        raise NotImplementedError()

    @abc.abstractmethod
    def create(self, data: Union[Dict[str, Any], List[Dict[str, Any]]]) -> Dict[str, Any]:
        '''新規データの作成関数
        Returns:
            int: serial型のID
            str: uuid型のID
            TODO: 型違いの挙動確認を行う
        '''
        raise NotImplementedError()

    @abc.abstractmethod
    def update(self, id: int, data: Dict[str, Any]) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def delete(self, id: Union[int, List[int]]) -> None:
        raise NotImplementedError()
