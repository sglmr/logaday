from django.views.generic import TemplateView
from django.views.decorators.http import require_http_methods


@require_http_methods(["GET"])
class HomePageView(TemplateView):
    template_name = "pages/home.html"


@require_http_methods(["GET"])
class AboutPageView(TemplateView):
    template_name = "pages/about.html"


@require_http_methods(["GET"])
class ProfilePageView(TemplateView):
    template_name = "pages/profile.html"
