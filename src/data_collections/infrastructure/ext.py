from data_collections.application.interfaces import ICollectionsHandler, IDBRepository
from data_collections.domain.models import Collection
from django.db.models import QuerySet
from django.conf import settings
from datetime import datetime
from typing import List
import petl as etl
import requests
import string
import random


homeworlds_cache = {}  # We can use any cache tool like Redis


class CollectionsHandler(ICollectionsHandler):
    def _process_homeworld_names(self, record: dict) -> dict:
        homeworld = record.get("homeworld", "N/A")

        # To prevent many requests we can cache retrieved planets names
        # and use it to get value faster
        if not homeworld in homeworlds_cache.keys():
            mapped_name = requests.get(homeworld).json()
            homeworlds_cache[homeworld] = mapped_name.get("name")

        record["homeworld"] = homeworlds_cache.get(homeworld)
        return record
    
    def _add_current_date(self, record: dict) -> dict:
        today_date = datetime.today().date()
        record["date"] = today_date
        return record

    def _write_to_csv(self, data: dict, filename: str) -> None:
        table_data = [list(data[0].keys())[0:9] + ["date"]]

        for record in data:
            data_to_process = {k: record[k] for k in list(record)[0:9]}
            adjusted_record: dict = self._process_homeworld_names(data_to_process)
            adjusted_record: dict = self._add_current_date(data_to_process)
            table_data.append(list(adjusted_record.values()))

        table = etl.head(table_data, 10)
        etl.tocsv(table, settings.DATASET_DIR[0] + f"/{filename}")

    def _prepare_data_for_presentation(self, headers, payload) -> List:
        adjusted_data = []
        for record in payload:
            record_dict = dict((headers[i], record[i]) for i in range(len(record)))
            adjusted_data.append(record_dict)
        return adjusted_data


    def retrieve_data(self, page: int) -> str:
        # Here we only want 1st page, because if for example
        # endpoint will have 2000 pages in future then we
        # will have to send 2000 requests
        result = requests.get(
            f"https://swapi.dev/api/people/?page={page}"
        ).json()  # get data from API
        random_string = "".join(random.choice(string.ascii_letters) for _ in range(24))
        filename = f"{random_string}.csv"

        self._write_to_csv(result.get("results"), filename)
        return filename

    def get_csv_data(self, filename: int):
        data = etl.fromcsv(settings.DATASET_DIR[0] + f"/{filename}")
        adjusted_data = self._prepare_data_for_presentation(data[0], data[1:])
        return adjusted_data, data[0] # headers for table
        

class DBRepository(IDBRepository):
    def write_to_db(self, filename: str) -> None:
        Collection.objects.create(filename=filename)

    def get_db_data(self) -> QuerySet:
        # here that line should be moved to repositories.py file
        # but it's overkill for now
        return Collection.objects.all().order_by("-edited")
    
    def get_filename(self, id: int) -> str:
        return Collection.objects.get(id=id).filename
