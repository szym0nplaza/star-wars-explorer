from data_collections.application.interfaces import ICollectionsRetreiver
from data_collections.domain.models import Collection
import requests


class CollectionsRetreiver(ICollectionsRetreiver):
    def retrieve_data(self, page):
        result = requests.get(
            f"https://swapi.dev/api/people/?page={page}"
        )  # get data from API
        print(len(result.json().get("results")))

    def get_db_data(self):
        # here that line should be moved to repositories.py file
        # but it's overkill for now 
        return Collection.objects.all()
