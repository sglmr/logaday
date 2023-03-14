import csv
import json

from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.utils import timezone
from django.utils.dateparse import parse_date
from django.views.decorators.http import require_http_methods

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
    except (AttributeError, TypeError):
        # Do nothing if the date is invalid
        return HttpResponse("", status=204)


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
        dt = timezone.datetime.now().date()
    record, created = Record.objects.get_or_create(user=request.user, date=dt)
    context = {"form": RecordForm(instance=record)}

    return TemplateResponse(request, "records/workbench.html", context=context)


@login_required()
@require_http_methods(["GET"])
def record_list_view(request: HttpRequest) -> TemplateResponse:
    records = Record.objects.filter(user=request.user).order_by("-date")
    context = {"records": records}
    return TemplateResponse(request, "records/list.html", context=context)


@login_required
@require_http_methods(["GET"])
def export_data_view(request: HttpRequest, format: str) -> HttpResponse | JsonResponse:

    objects = Record.objects.filter(user=request.user).order_by("-date")
    serialized_data = serializers.serialize(
        "json",
        objects,
        fields=["created", "modified", "date", "title", "content"],
    )
    json_data = json.loads(serialized_data)
    json_data = [d["fields"] for d in json_data]

    # Return a CSV Export
    if format.lower() == "csv":
        response = HttpResponse(
            content_type="text/csv",
            headers={
                "Content-Disposition": f'attachment; filename="{timezone.now()}.csv"'
            },
        )
        writer = csv.DictWriter(response, fieldnames=json_data[1].keys())
        writer.writeheader()
        for row in json_data:
            writer.writerow(row)

        return response

    # Return a json export
    elif format.lower() == "json":
        return HttpResponse(
            json.dumps(json_data),
            content_type="application/json",
            headers={
                "Content-Disposition": f'attachment; filename="{timezone.now()}.json"'
            },
        )

    else:
        return HttpResponse("", status=406)
