from data_collections.application.interfaces import ICollectionsHandler, IDBRepository
from data_collections.domain.models import Collection, Planets
from django.db.models import QuerySet
from django.conf import settings
from datetime import datetime
from typing import List
import petl as etl
import requests
import string
import random


class CollectionsHandler(ICollectionsHandler):
    def _process_homeworld_names(self, record: dict) -> dict:
        homeworld_url = record.get("homeworld", "N/A")

        # To prevent many requests we can store in db retrieved
        # planets names and use it to get value faster.
        # I wondered if cache will be better for it, but
        # for large amounts of data db will perform better.
        # This function causes biggest bottleneck in data retrieving process.
        # Of course we can request full pages but if our item is on page 123
        # we will have to request API 123 times to map it.
        try:
            verbose_planet_name = Planets.objects.get(url=homeworld_url)
        except Planets.DoesNotExist:
            mapped_name = requests.get(homeworld_url).json()
            verbose_planet_name = Planets.objects.create(
                url=homeworld_url, verbose_name=mapped_name.get("name")
            )

        record["homeworld"] = verbose_planet_name.verbose_name
        return record

    def _add_current_date(self, record: dict) -> dict:
        today_date = datetime.today().date()
        record["date"] = today_date
        return record

    def _prepare_for_csv(self, data: dict) -> etl.Table:
        # process and prepare data for csv file
        table_data = [list(data[0].keys())[0:9] + ["date"]]

        for record in data:
            data_to_process = {k: record[k] for k in list(record)[0:9]}
            adjusted_record: dict = self._process_homeworld_names(data_to_process)
            adjusted_record: dict = self._add_current_date(data_to_process)
            table_data.append(list(adjusted_record.values()))

        table = etl.head(table_data, 10)
        return table

    def _make_request(self, page: int = 1) -> dict:
        # Here we only want 1st page, because if for example
        # endpoint will have 2000 pages in future then we
        # will have to send 2000 requests
        result = (
            requests.get(f"https://swapi.dev/api/people/?page={page}")
            .json()
            .get("results")
        )  # get data from API
        return result

    def retrieve_data(self) -> str:
        # Get 1st 10 records of dataset
        api_result: dict = self._make_request()  # Make request to API
        random_string = "".join(
            random.choice(string.ascii_letters) for _ in range(24)
        )  # Generates random filename
        filename = f"{random_string}.csv"

        table = self._prepare_for_csv(api_result)
        etl.tocsv(table, settings.DATASET_DIR[0] + f"/{filename}")
        return filename

    def retrieve_additional_pages(self, chunk: int, filename: str) -> None:
        # Get another pages of data and append it to csv
        result = self._make_request(chunk)
        table = self._prepare_for_csv(result)
        etl.appendcsv(table, settings.DATASET_DIR[0] + f"/{filename}")

    def get_csv_data(self, filename: int, records_count: int, filters: str) -> dict:
        """Gets transformed data from csv file."""

        records_count *= 10
        base_data = etl.fromcsv(
            settings.DATASET_DIR[0] + f"/{filename}"
        )  # read data from csv file

        if not filters:
            return {
                "payload": tuple(base_data[1 : records_count + 1]),
                "table_headers": base_data[0],
                "filters": base_data[0],
            }
        else:
            data = etl.cut(
                base_data, *filters.split(",")
            )  # filter data by given fields
            counted_data = etl.valuecounts(
                data, *filters.split(",")
            )  # count occurencies of each pair
            formatted_data = etl.cutout(
                counted_data, "frequency"
            )  # remove frequency column
            return {
                "payload": tuple(formatted_data[1:]),
                "table_headers": formatted_data[0],
                "filters": base_data[0],
            }


class DBRepository(IDBRepository):
    # here that class should be moved to repositories.py file
    # but it's overkill for now

    def write_to_db(self, filename: str) -> None:
        Collection.objects.create(filename=filename)

    def get_db_data(self) -> QuerySet:
        return Collection.objects.all().order_by("-edited")

    def get_filename(self, id: int) -> str:
        return Collection.objects.get(id=id).filename

    def update_record(self, id: int) -> int:
        """
        Updates db record, increments chunks by 1 and changes edited date
        """
        db_record = Collection.objects.get(id=id)
        db_record.update_record()
        return db_record.chunks

    def get_chunks(self, id: int) -> int:
        return Collection.objects.get(id=id).chunks
