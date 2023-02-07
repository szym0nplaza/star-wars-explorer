from .interfaces import ICollectionsHandler
from .dto import CollectionDTO
from typing import List


class CollectionsService:
    def __init__(self, data_handler: ICollectionsHandler) -> None:
        self._data_handler = data_handler

    def retirieve_ext_data(self, page: int = 1) -> None:
        self._data_handler.retrieve_data(page)

    def get_db_data(self) -> List[CollectionDTO]:
        qs = self._data_handler.get_db_data()
        result = [
            CollectionDTO(filename=record.filename, edited=record.edited)
            for record in qs
        ]  # map queryset to dto, separate presentation data from db
        return result
