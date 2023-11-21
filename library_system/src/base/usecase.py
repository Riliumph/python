import abc
from typing import Any, Dict

from base.gateway import BaseRepository


class BaseInputPort(abc.ABC):
    @abc.abstractmethod
    def __init__(self, repo: BaseRepository) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def __call__(self, request: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError()
