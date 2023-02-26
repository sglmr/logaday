from django.http import HttpRequest, HttpResponse
from django.template.response import TemplateResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.utils.timezone import datetime

from logapp.models import get_or_create_users_log, Log


@login_required()
@require_http_methods(["POST", "GET"])
def log_form_view(
    request: HttpRequest, date: datetime.date = None
) -> TemplateResponse | HttpResponse:
    if request.method == "GET":
        log = get_or_create_users_log(user=request.user, date=request.GET["date"])
        return TemplateResponse(request, "logapp/log_update_form.html", {"log": log})
    elif request.method == "POST":
        log = get_or_create_users_log(user=request.user, date=request.POST["date"])
        log.title = request.POST["title"]
        log.content = request.POST["content"]
        log.save()

        return HttpResponse("")


@login_required()
@require_http_methods(["GET"])
def log_update_view(request: HttpRequest, date: str = None) -> TemplateResponse:
    if not date:
        date = datetime.now()
    log = get_or_create_users_log(user=request.user, date=date)
    context = {"log": log}

    return TemplateResponse(request, "logapp/log_update.html", context=context)


@login_required()
@require_http_methods(["GET"])
def log_list_view(request: HttpRequest) -> TemplateResponse:
    logs = Log.objects.filter(user=request.user)
    context = {"objects": logs}
    return TemplateResponse(request, "logapp/log_list.html", context=context)
