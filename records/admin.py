from django.contrib import admin

from .models import Record, RecordSetting


@admin.register(RecordSetting)
class RecordSettingAdmin(admin.ModelAdmin):
    fields = ["user", "headings"]
    list_display = ["user", "headings"]
    search_fields = ["user", "headings"]


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    fields = ["user", "date", "title", "content"]
    list_display = ["date", "title", "user", "content"]
    search_fields = ["title", "content"]
