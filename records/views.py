from django.http import HttpRequest, HttpResponse
from django.template.response import TemplateResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.utils.timezone import datetime
from django.utils.dateparse import parse_date
from django.views.generic import FormView
from django.shortcuts import get_object_or_404


from .forms import RecordForm
from .models import Record


@login_required()
@require_http_methods(["POST"])
def record_form_change_view(request: HttpRequest) -> TemplateResponse:
    try:
        date = parse_date(request.POST.get("date"))
        record, created = Record.objects.get_or_create(user=request.user, date=date)
        form = RecordForm(instance=record)
        return TemplateResponse(
            request, "records/record_form_partial.html", {"form": form}
        )
    except AttributeError:
        # Do nothing if the date is invalid
        h = HttpResponse("")
        h.status_code = 204
        return h


@login_required()
@require_http_methods(["POST"])
def record_form_save_view(request: HttpRequest) -> HttpResponse:
    record = get_object_or_404(
        Record,
        date=parse_date(request.POST.get("date")),
        user=request.user,
    )
    form = RecordForm(data=request.POST, instance=record)
    if form.is_valid():
        form.save()
    else:
        # TODO: figure out how to send back form validation errors
        pass
    return HttpResponse("")


@login_required()
@require_http_methods(["GET"])
def record_editor_view(request: HttpRequest, date: str = None) -> TemplateResponse:
    if date:
        dt = parse_date(date)
    else:
        dt = datetime.now()
    record, created = Record.objects.get_or_create(user=request.user, date=dt)
    context = {"form": RecordForm(instance=record)}

    return TemplateResponse(request, "records/workbench.html", context=context)


@login_required()
@require_http_methods(["GET"])
def record_list_view(request: HttpRequest) -> TemplateResponse:
    records = Record.objects.filter(user=request.user).order_by("-date")
    context = {"records": records}
    return TemplateResponse(request, "records/list.html", context=context)
