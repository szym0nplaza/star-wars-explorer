from django.urls import path
from .views import CollectionsList


urlpatterns = [
    path("collections/", CollectionsList.as_view())
]

