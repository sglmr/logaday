from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.http import HttpRequest
from django.utils.timezone import datetime
from django.utils.dateparse import parse_date


def listisize(text: str):
    new_list = list()

    for line in text.splitlines():
        if line[:1].isalpha():
            line = "- " + line
        new_list.append(line)
    return "\n".join(new_list)


class Log(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    title = models.CharField(_("log title"), max_length=255, blank=True)
    content = models.TextField(_("log content"), blank=True)
    date = models.DateField(_("log date"))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-date", "user"]
        unique_together = ("user", "date")

    def __str__(self):
        return f"{self.title}"

    def save(self, *args, **kwargs):
        # Add a title if one doesn't exist
        if not self.title:
            self.title = self.pretty_log_date

        # "Listisize"
        self.content = listisize(text=self.content)

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        # return reverse("view_log", kwargs={"pk": self.pk})
        ...

    @property
    def date_y_m_d(self):
        return self.date.strftime("%Y-%m-%d")

    @property
    def pretty_log_date(self):
        return self.date.strftime("%A, %b %d, %Y")


def get_or_create_users_log(user, date: str) -> Log:
    if type(date) == str:
        date = parse_date(date)

    try:
        return Log.objects.get(user=user, date=date)
    except Log.DoesNotExist:
        return Log.objects.create(
            user=user,
            date=date,
            content=user.default_log_content,
        )
