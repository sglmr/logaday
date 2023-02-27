from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.contrib.auth.models import User


class CustomUser(AbstractUser):
    pass

    def __str__(self):
        return self.email

    log_sections = models.CharField(
        _("log sections"),
        max_length=300,
        help_text=_("Required. Comma separated list of default sections for logs"),
        default="personal, work",
    )

    @property
    def default_log_content(self):
        # Split log content field into a list
        l = [x for x in self.log_sections.split(",")]

        # format the log content sections
        l = [x.strip().capitalize() for x in l]

        # Add a prefix to the heading
        l = ["# " + x for x in l]

        # Separate the headings with newlines
        return "\n- \n\n".join(l) + "\n- "
