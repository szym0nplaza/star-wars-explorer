from django.views.generic import TemplateView
from django.views import View
from django.http import JsonResponse
from django.shortcuts import render
from data_collections.infrastructure.ext import CollectionsHandler, DBRepository
from data_collections.application.services import CollectionsService


class CollectionsList(TemplateView):
    template_name = "list.html"
    _handler = CollectionsService(
        data_handler=CollectionsHandler(), repo=DBRepository()
    )

    def get(self, request):
        db_data = self._handler.get_db_data()
        return render(request, self.template_name, context={"collections": db_data})


class DatasetFetchView(View):
    _handler = CollectionsService(
        data_handler=CollectionsHandler(), repo=DBRepository()
    )

    def get(self, _request):
        self._handler.retirieve_ext_data()
        return JsonResponse({"message": "ok"})


class CollectionDetails(TemplateView):
    template_name = "collection-details.html"
    _handler = CollectionsService(
        data_handler=CollectionsHandler(), repo=DBRepository()
    )

    def get(self, request, id):
        records_count = int(request.GET.get("records"))
        filters = request.GET.get("filters")
        dto = self._handler.get_csv_data(id, records_count, filters)
        return render(
            request,
            self.template_name,
            context={
                **dto.__dict__,
                "dataset_id": id,
                "chosen_filters": filters,
            },
        )
