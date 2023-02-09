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
    def _make_request(self, content: str) -> tuple:
        result = requests.get(
            f"https://swapi.dev/api/{content}/?page=1"
        ).json()  # get first page from API

        collected_data = [*result.get("results")]
        while result.get(
            "next"
        ):  # Due to specific api, we have to go page by page to collect data, In future we can move it to celery.
            next_page_data = requests.get(result.get("next")).json()
            result = requests.get(result.get("next")).json()
            collected_data = [*collected_data, *next_page_data.get("results")]

        return collected_data, result.get("count")

    def _process_homeworld_names(self, record: dict) -> dict:
        homeworld_url = record.get("homeworld", "N/A")

        # To prevent many requests we can store in db retrieved
        # planets names and use it to get value faster.
        # I wondered if cache will be better for it, but
        # for large amounts of data db will perform better.
        planets_count = requests.get(
            "https://swapi.dev/api/planets/?page=1"
        ).json().get("count")

        if planets_count != Planets.objects.all().count(): # Check if planets are loaded
            # For future I will have to adjust it if one
            # single planet is added, right now it will download all,
            # maybe it's worth to move it to some signal to call it once
            collected_data, _count = self._make_request("planets")
            processed_data = [
                Planets(verbose_name=record.get("name"), url=record.get("url"))
                for record in collected_data
            ]

            Planets.objects.bulk_create(processed_data)

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

    def _prepare_for_csv(self, data: dict, pages: int) -> etl.Table:
        # process and prepare data for csv file

        for i, record in enumerate(data):
            data[i] = {k: record[k] for k in list(record)[0:9]}
            data[i] = self._process_homeworld_names(data[i])
            data[i] = self._add_current_date(data[i])

        table = etl.fromdicts(data)
        return table

    def retrieve_data(self) -> str:
        collected_data, count = self._make_request("people")
        random_string = "".join(
            random.choice(string.ascii_letters) for _ in range(24)
        )  # Generates random filename
        filename = f"{random_string}.csv"

        table = self._prepare_for_csv(collected_data, count)
        etl.tocsv(table, settings.DATASET_DIR[0] + f"/{filename}")
        return filename

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
        # This is here because I tested case when firstly
        # we load 1 page and each time we click load more
        # new data appends to csv (if is not retrieved yet)
        return Collection.objects.get(id=id).chunks
