from abc import ABC, abstractmethod

class IFileStorage(ABC):
    @abstractmethod
    def make_dir(self, path: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def save_file(self, path: str, data: bytes) -> None:
        raise NotImplementedError

    @abstractmethod
    def exists_file(self, path: str) -> bool:
        raise NotImplementedError
