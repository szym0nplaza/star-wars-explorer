from django.urls import path
from .views import CollectionsList, DatasetFetchView, CollectionDetails
from django.views.generic.base import RedirectView


urlpatterns = [
    path('', RedirectView.as_view(url='/collections/')),
    path('collections/', CollectionsList.as_view()),
    path('collections/<int:id>', CollectionDetails.as_view()),
    path('fetch-dataset/', DatasetFetchView.as_view()),
    path('fetch-dataset/<int:id>', DatasetFetchView.as_view())
]

