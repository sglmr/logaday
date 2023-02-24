from django.urls import path, register_converter, re_path
from django.utils.timezone import datetime

from logapp.views import log_form_view, log_update_view


class DateConverter:
    regex = "\d{4}-\d{1,2}-\d{1,2}"
    format = "%Y-%m-%d"

    def to_python(self, value):
        return datetime.strptime(value, self.format).date()

    def to_url(self, value):
        return value.strftime(self.format)


register_converter(DateConverter, "date")

app_name = "log"
urlpatterns = [
    path("update/", log_update_view, name="update_today"),
    re_path(
        r"^update/(?P<date>\d{4}-\d{1,2}-\d{1,2})/$", log_update_view, name="update"
    ),
    path("update_form/", log_form_view, name="update_form"),
]
