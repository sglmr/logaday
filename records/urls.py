from django.urls import path, register_converter, re_path
from django.utils.timezone import datetime

from .views import record_form_view, record_update_view, record_list_view
from .signals import create_records_settings_signal


class DateConverter:
    regex = "\d{4}-\d{1,2}-\d{1,2}"
    format = "%Y-%m-%d"

    def to_python(self, value):
        return datetime.strptime(value, self.format).date()

    def to_url(self, value):
        return value.strftime(self.format)


register_converter(DateConverter, "date")

app_name = "records"
urlpatterns = [
    path("update/", record_update_view, name="update_today"),
    path("list/", record_list_view, name="list"),
    re_path(
        r"^update/(?P<date>\d{4}-\d{1,2}-\d{1,2})/$", record_update_view, name="update"
    ),
    path("update_form/", record_form_view, name="update_form"),
]
