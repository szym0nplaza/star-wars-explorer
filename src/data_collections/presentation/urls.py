from django.urls import path
from .views import CollectionsList, DatasetFetchView


urlpatterns = [
    path('collections/', CollectionsList.as_view()),
    path('fetch-dataset/', DatasetFetchView.as_view())
]

