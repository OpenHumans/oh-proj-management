from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = "oh_proj_management/home.html"
