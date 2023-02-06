from abc import ABC, abstractmethod


class ICollectionsRetreiver(ABC):
    @abstractmethod
    def retrieve_data(self):
        raise NotImplementedError
