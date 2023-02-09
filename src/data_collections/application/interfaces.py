from abc import ABC, abstractmethod
from django.db.models import QuerySet

# Here are abstract classes for dependency inversion purpouse


class ICollectionsHandler(ABC):
    @abstractmethod
    def retrieve_data(self, page: int = 1) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_csv_data(self, filename: str, records_count: int, filters: str) -> dict:
        raise NotImplementedError


class IDBRepository(ABC):
    @abstractmethod
    def get_db_data(self) -> QuerySet:
        raise NotImplementedError

    @abstractmethod
    def write_to_db(self, filename) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_filename(self, id: int) -> str:
        raise NotImplementedError
