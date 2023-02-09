from .interfaces import ICollectionsHandler, IDBRepository
from .dto import CollectionDTO, DatasetDTO
from typing import List


class CollectionsService:
    # This module uses dependency inversion, in future we can test
    # this class with mock adapters which inherit Interfaces

    def __init__(self, data_handler: ICollectionsHandler, repo: IDBRepository) -> None:
        self._data_handler = data_handler
        self._repo = repo

    def retirieve_ext_data(self) -> None:
        filename = self._data_handler.retrieve_data()
        self._repo.write_to_db(filename)

    def get_db_data(self) -> List[CollectionDTO]:
        qs = self._repo.get_db_data()
        result = [
            CollectionDTO(id=record.id, filename=record.filename, edited=record.edited)
            for record in qs
        ]  # map queryset to dto, separate presentation data from db
        return result

    def get_csv_data(self, id: int, records_count: int, filters: str) -> DatasetDTO:
        filename = self._repo.get_filename(id)
        csv_data = self._data_handler.get_csv_data(filename, records_count, filters)
        return DatasetDTO(
            filename=filename,
            dataset=csv_data.get("payload"),
            headers=csv_data.get("table_headers"),
            records=records_count,
            filters=csv_data.get("filters"),
        )
