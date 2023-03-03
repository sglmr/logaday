from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


def listisize(text: str):
    new_list = list()

    for line in text.splitlines():
        if line[:1].isalpha():
            line = "- " + line
        new_list.append(line)
    return "\n".join(new_list)


class RecordSetting(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name="record_settings",
        on_delete=models.CASCADE,
    )

    headings = models.CharField(
        _("record headings"),
        max_length=300,
        help_text=_("Required. Comma separated list of default headings to use."),
        default="personal, work",
    )

    class Meta:
        verbose_name = _("record setting")
        verbose_name_plural = _("record settings")

    def __str__(self):
        return "%s record settings" % self.user

    @property
    def default_content(self):
        # Split content field into a list
        l = [x for x in self.headings.split(",")]

        # format the content sections
        l = [x.strip().capitalize() for x in l]

        # Add a prefix to the heading
        l = ["# " + x for x in l]

        # Separate the headings with newlines
        return "\n- \n\n".join(l) + "\n- "


class Record(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="records", on_delete=models.CASCADE
    )
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    title = models.CharField(_("record title"), max_length=255, blank=True)
    content = models.TextField(_("record content"), blank=True)
    date = models.DateField(_("record date"))

    class Meta:
        verbose_name = _("record")
        verbose_name_plural = _("records")
        unique_together = ("user", "date")

    def __str__(self):
        return f"{self.title}"

    def save(self, *args, **kwargs):
        # Add a title if one doesn't exist
        if not self.title:
            self.title = self.pretty_date

        # Add default content if it doesn't exist
        if not self.content:
            self.content = self.user.record_settings.default_content

        # "Listisize"
        self.content = listisize(text=self.content)

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        # TODO: return reverse("view_record", kwargs={"pk": self.pk})
        pass  # pragma: no cover

    @property
    def content_lines(self):
        return self.content.splitlines()

    @property
    def date_y_m_d(self):
        return self.date.strftime("%Y-%m-%d")

    @property
    def pretty_date(self):
        return self.date.strftime("%A, %b %d, %Y")
