from abc import ABC, abstractmethod

# Here are abstract classes for dependency inversion purpouse

class ICollectionsHandler(ABC):
    @abstractmethod
    def retrieve_data(self, page: int) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def get_db_data(self):
        raise NotImplementedError
