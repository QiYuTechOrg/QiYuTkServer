from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.html import format_html

__all__ = ["core_to_admin_url", "user_to_admin_url"]


def core_to_admin_url(obj: models.Model) -> str:
    name = obj.__class__.__name__.lower()
    url = reverse(f"admin:core_{name}_change", args=(obj.id,))
    return format_html(
        '<a href="{url}">{obj}</a>', url=url, obj=f"{str(obj)}(ID:{obj.id})"
    )


def user_to_admin_url(obj: User) -> str:
    url = reverse("admin:auth_user_change", args=(obj.id,))
    return format_html(
        '<a href="{url}">{user}</a>', url=url, user=f"{obj.username}(ID:{obj.id})"
    )
