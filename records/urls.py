from django.urls import path, re_path, register_converter
from django.utils.timezone import datetime

from .views import (
    export_data_view,
    record_editor_view,
    record_form_change_view,
    record_form_save_view,
    record_list_view,
)


class DateConverter:  # pragma: no cover
    regex = "\d{4}-\d{1,2}-\d{1,2}"
    format = "%Y-%m-%d"

    def to_python(self, value):
        return datetime.strptime(value, self.format).date()

    def to_url(self, value):
        return value.strftime(self.format)


register_converter(DateConverter, "date")

app_name = "records"
urlpatterns = [
    path("list/", record_list_view, name="list"),
    path("save_form/", record_form_save_view, name="save_form"),
    path("change_form/", record_form_change_view, name="change_form"),
    path("export/<str:format>/", export_data_view, name="export"),
    re_path(r"^(?P<date>\d{4}-\d{1,2}-\d{1,2})/$", record_editor_view, name="edit"),
    path("", record_editor_view, name="edit_today"),
]
