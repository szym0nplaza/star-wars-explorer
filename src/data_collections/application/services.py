from .interfaces import ICollectionsHandler, IDBRepository
from .dto import CollectionDTO
from typing import List, Tuple


class CollectionsService:
    def __init__(self, data_handler: ICollectionsHandler, repo: IDBRepository) -> None:
        self._data_handler = data_handler
        self._repo = repo

    def retirieve_ext_data(self, page: int = 1) -> None:
        filename = self._data_handler.retrieve_data(page)
        self._repo.write_to_db(filename)

    def get_db_data(self) -> List[CollectionDTO]:
        qs = self._repo.get_db_data()
        result = [
            CollectionDTO(id=record.id, filename=record.filename, edited=record.edited)
            for record in qs
        ]  # map queryset to dto, separate presentation data from db
        return result
    
    def get_csv_data(self, id: int) -> Tuple:
        filename = self._repo.get_filename(id)
        dataset, headers = self._data_handler.get_csv_data(filename)
        return dataset, filename, headers
