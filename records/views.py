from django.http import HttpRequest, HttpResponse
from django.template.response import TemplateResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.utils.timezone import datetime
from django.utils.dateparse import parse_date

from .models import Record


@login_required()
@require_http_methods(["POST", "GET"])
def record_form_view(
    request: HttpRequest, date: datetime.date = None
) -> TemplateResponse | HttpResponse:
    if request.method == "GET":
        date = parse_date(request.GET["date"] or request.POST["date"])
        record, created = Record.objects.get_or_create(user=request.user, date=date)
        return TemplateResponse(request, "records/update_form.html", {"record": record})
    elif request.method == "POST":
        date = parse_date(request.POST["date"])
        record, created = Record.objects.get_or_create(user=request.user, date=date)
        record.title = request.POST["title"]
        record.content = request.POST["content"]
        record.save()
        return HttpResponse("")


@login_required()
@require_http_methods(["GET"])
def record_update_view(request: HttpRequest, date: str = None) -> TemplateResponse:
    if date:
        dt = parse_date(date)
    else:
        dt = datetime.now()
    record, created = Record.objects.get_or_create(user=request.user, date=dt)
    context = {"record": record}

    return TemplateResponse(request, "records/update.html", context=context)


@login_required()
@require_http_methods(["GET"])
def record_list_view(request: HttpRequest) -> TemplateResponse:
    records = Record.objects.filter(user=request.user).order_by("-date")
    context = {"records": records}
    return TemplateResponse(request, "records/list.html", context=context)
