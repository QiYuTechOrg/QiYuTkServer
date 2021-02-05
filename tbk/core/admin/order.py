from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from core.models import OrderModel


@admin.register(OrderModel)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "order_no",
        "user_link",
        "order_platform",
        "order_ctime",
        "order_status",
    )
    list_filter = ("order_platform", "order_status")
    search_fields = ("user__username",)
    raw_id_fields = ("user",)
    # show mtime field in admin
    readonly_fields = ("mtime",)

    def user_link(self, obj: OrderModel):
        url = reverse("admin:auth_user_change", args=(obj.user.id,))
        return format_html('<a href="{url}">{user}</a>', url=url, user=obj.user)

    user_link.allow_tags = True
    user_link.short_description = "用户"
