from django.contrib import admin
from logapp.models import Log


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    fields = ["user", "date", "title", "content"]
    list_display = ["date", "title", "user", "content"]
    search_fields = ["title", "content"]
