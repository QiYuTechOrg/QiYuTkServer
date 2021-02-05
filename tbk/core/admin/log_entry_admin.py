from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.admin.models import LogEntry

__all__ = ["LogEntryAdmin"]


@admin.register(LogEntry)
class LogEntryAdmin(ModelAdmin):
    date_hierarchy = "action_time"
    search_fields = ("object_repr", "change_message")
    list_display = (
        "action_time",
        "user",
        "content_type",
        "action_flag",
    )
