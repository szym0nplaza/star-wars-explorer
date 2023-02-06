from django.views.generic import TemplateView


class CollectionsList(TemplateView):
    template_name = "list.html"
