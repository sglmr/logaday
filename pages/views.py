from django.views.generic import TemplateView
from django.http import HttpRequest, HttpResponse
from django.template.response import TemplateResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.utils.timezone import datetime


@require_http_methods(["GET"])
def home_page_view(request: HttpRequest) -> TemplateResponse:
    return TemplateResponse(request, "pages/home.html")


@login_required()
@require_http_methods(["GET"])
def profile_page_view(request: HttpRequest) -> TemplateResponse:
    return TemplateResponse(request, "pages/profile.html")
