from data_collections.application.interfaces import ICollectionsHandler, IDBRepository
from data_collections.domain.models import Collection, Planets
from django.db.models import QuerySet
from django.conf import settings
from datetime import datetime
import petl as etl
import requests
import string
import random


class CollectionsHandler(ICollectionsHandler):
    def _make_request(self, content: str) -> list:
        result = requests.get(
            f"https://swapi.dev/api/{content}/?page=1"
        ).json()  # get first page from API

        collected_data = [*result.get("results")]
        while result.get(
            "next"
        ):  # Due to specific api, we have to go page by page to collect data, In future we can move it to celery.
            print("Requesting API...")
            next_page_data = requests.get(result.get("next")).json()
            print("Data retrieved.")
            result = next_page_data
            collected_data = [*collected_data, *next_page_data.get("results")]
        return collected_data

    def _process_homeworld_names(self, homeworld_url: str) -> str:
        # To prevent many requests we can store in db retrieved
        # planets names and use it to get value faster.
        # I wondered if cache will be better for it, but
        # for large amounts of data db will perform better.

        if not Planets.objects.all():  # Check if planets are loaded
            # maybe it's worth to move it to some signal to call it once
            collected_data = self._make_request("planets")
            processed_data = [
                Planets(verbose_name=record.get("name"), url=record.get("url"))
                for record in collected_data
            ]

            Planets.objects.bulk_create(processed_data)

        try:
            verbose_planet_name = Planets.objects.get(url=homeworld_url).verbose_name
        except Planets.DoesNotExist:
            mapped_name = requests.get(homeworld_url).json()
            verbose_planet_name = Planets.objects.create(
                url=homeworld_url, verbose_name=mapped_name.get("name")
            ).verbose_name

        return verbose_planet_name

    def _prepare_for_csv(self, data: dict) -> etl.Table:
        # process and prepare data for csv file
        table_headers = list(data[0].keys())[0:9]
        today_date = datetime.today().date()

        table = etl.fromdicts(data)
        table = etl.cut(table, table_headers)
        table = etl.addfield(table, "date", today_date)
        table = etl.convert(table, "homeworld", self._process_homeworld_names)
        return table

    def retrieve_data(self) -> str:
        collected_data = self._make_request("people")
        random_string = "".join(
            random.choice(string.ascii_letters) for _ in range(24)
        )  # Generates random filename
        filename = f"{random_string}.csv"

        table = self._prepare_for_csv(collected_data)
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
