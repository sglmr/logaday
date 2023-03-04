from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import RecordSetting


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_records_settings_signal(sender, instance, created, **kwargs):
    if created:
        RecordSetting.objects.create(user=instance)
