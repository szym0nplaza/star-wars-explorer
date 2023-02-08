from django.urls import path
from .views import CollectionsList, DatasetFetchView, CollectionDetails


urlpatterns = [
    path('collections/', CollectionsList.as_view()),
    path('collections/<int:id>', CollectionDetails.as_view()),
    path('fetch-dataset/', DatasetFetchView.as_view())
]

