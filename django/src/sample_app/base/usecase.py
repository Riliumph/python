import abc
from typing import List, Dict, Any

from sample_app.base.repository import BaseRepository


class BaseInputPort(abc.ABC):
    @abc.abstractmethod
    def __init__(self, repo: BaseRepository) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def __call__(self, request: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError()
