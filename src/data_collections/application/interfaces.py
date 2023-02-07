from abc import ABC, abstractmethod

# Here are abstract classes for dependency inversion purpouse

class ICollectionsRetreiver(ABC):
    @abstractmethod
    def retrieve_data(self) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def get_db_data(self):
        raise NotImplementedError
