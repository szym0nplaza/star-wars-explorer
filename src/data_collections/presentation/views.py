from django.views.generic import TemplateView
from django.shortcuts import render
from data_collections.infrastructure.ext import CollectionsRetreiver
from data_collections.application.services import CollectionsHandler


class CollectionsList(TemplateView):
    template_name = "list.html"
    _handler = CollectionsHandler(data_handler=CollectionsRetreiver())

    def get(self, request):
        db_data = self._handler.get_db_data()
        return render(request, self.template_name, context={"collections": db_data})
