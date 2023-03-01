from django.db import models
from django.utils.translation import gettext_lazy as _

from authtools.models import AbstractNamedUser


class User(AbstractNamedUser):
    id = models.BigAutoField(primary_key=True)

    class Meta(AbstractNamedUser.Meta):
        swappable = "AUTH_USER_MODEL"
        verbose_name = _("user")
        verbose_name_plural = _("users")
