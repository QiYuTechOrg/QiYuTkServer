from django.contrib import admin
from django.contrib.admin import ModelAdmin

from core.models import TBChannelIdModel

__all__ = ["TbChannelIdAdmin"]


@admin.register(TBChannelIdModel)
class TbChannelIdAdmin(ModelAdmin):
    """
    淘宝渠道 ID 绑定
    允许管理员进行 删除 操作
    方便对用户进行 `解绑` 操作
    """

    list_display = ("user", "relation_id", "special_id", "ctime")
    search_fields = ("user", "relation_id")
    raw_id_fields = ("user",)
