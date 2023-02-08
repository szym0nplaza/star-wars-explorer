from abc import ABC, abstractmethod
from django.db.models import QuerySet

# Here are abstract classes for dependency inversion purpouse

class ICollectionsHandler(ABC):
    @abstractmethod
    def retrieve_data(self, page: int = 1) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def get_csv_data(self, filename: str, records_count: int):
        raise NotImplementedError
    
    @abstractmethod
    def retrieve_additional_pages(self, chunk: int, filename: str):
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
    
    @abstractmethod
    def update_record(self, id: int) -> int:
        raise NotImplementedError
    
    @abstractmethod
    def get_chunks(self, id: int) -> int:
        raise NotImplementedError