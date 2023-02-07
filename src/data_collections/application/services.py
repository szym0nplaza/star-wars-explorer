from .interfaces import ICollectionsRetreiver
from .dto import CollectionDTO
from typing import List


class CollectionsHandler:
    def __init__(self, data_handler: ICollectionsRetreiver) -> None:
        self._data_handler = data_handler

    def retirieve_ext_data(self) -> None:
        self._data_handler.retrieve_data()

    def get_db_data(self) -> List[CollectionDTO]:
        qs = self._data_handler.get_db_data()
        result = [
            CollectionDTO(filename=record.filename, edited=record.edited)
            for record in qs
        ] # map queryset to dto, separate presentation data from db
        return result
