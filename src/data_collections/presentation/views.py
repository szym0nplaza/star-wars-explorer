from django.views.generic import TemplateView
from django.views import View
from django.http import JsonResponse
from django.shortcuts import render
from data_collections.infrastructure.ext import CollectionsHandler
from data_collections.application.services import CollectionsService


class CollectionsList(TemplateView):
    template_name = "list.html"
    _handler = CollectionsService(data_handler=CollectionsHandler())

    def get(self, request):
        db_data = self._handler.get_db_data()
        return render(request, self.template_name, context={"collections": db_data})


class DatasetFetchView(View):
    _handler = CollectionsService(data_handler=CollectionsHandler())

    def post(self, request, *args, **kwargs):
        self._handler.retirieve_ext_data()
        return JsonResponse({"message": "ok"})


class CollectionDetails(TemplateView):
    template_name = "collection-details.html"