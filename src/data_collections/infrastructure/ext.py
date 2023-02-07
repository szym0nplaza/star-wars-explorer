from data_collections.application.interfaces import ICollectionsHandler
from data_collections.domain.models import Collection
from django.conf import settings
import petl as etl
import requests
import string
import random


class CollectionsHandler(ICollectionsHandler):
    def _write_to_db(self, filename: str):
        Collection.objects.create(filename=filename)
        

    def _write_to_csv(self, data, filename):
        table_data = [list(data[0].keys())[0:9]]
        print(len(data))
        for record in data:
            print(list(record.values())[0])
            table_data.append(list(record.values())[0:9])

        table = etl.head(table_data, 10)
        etl.tocsv(table, settings.DATASET_DIR[0] + f"/{filename}")

    def retrieve_data(self, page: int):
        # Here we only want 1st page, because if for example
        # endpoint will have 2000 pages in future then we 
        # will have to send 2000 requests
        result = requests.get(
            f"https://swapi.dev/api/people/?page={page}"
        ).json()  # get data from API
        random_string = "".join(random.choice(string.ascii_letters) for _ in range(24))
        filename = f"{random_string}.csv"

        self._write_to_csv(result.get("results"), filename)
        self._write_to_db(filename)

    def get_db_data(self):
        # here that line should be moved to repositories.py file
        # but it's overkill for now 
        return Collection.objects.all().order_by("-edited")
