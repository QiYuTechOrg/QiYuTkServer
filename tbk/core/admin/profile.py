from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from core.models import Profile, UserTokenModel

__all__ = ["UserAdmin"]


class UserTokenAdminInline(admin.StackedInline):
    model = UserTokenModel
    can_delete = False
    verbose_name = "用户令牌"
    verbose_name_plural = "用户令牌"
    readonly_fields = ("token", "ctime", "mtime")

    def has_change_permission(self, request, obj=None):
        return False


# noinspection PyRedundantParentheses
class UserProfileAdminInline(admin.StackedInline):
    """
    用户信息 admin
    """

    model = Profile
    can_delete = False
    verbose_name = "用户信息"
    verbose_name_plural = "用户信息"


# noinspection PyRedundantParentheses
class UserAdmin(BaseUserAdmin):
    def user_test_account(self, obj: User):
        return obj.profile.test_account

    user_test_account.short_description = "测试账号"
    user_test_account.boolean = True

    list_display = (
        "id",
        "username",
        "email",
        "user_test_account",
        "is_active",
        "is_staff",
        "is_superuser",
    )
    list_display_links = ("id", "username")
    inlines = (UserProfileAdminInline, UserTokenAdminInline)

    def get_readonly_fields(self, request, obj=None):
        fields = super().get_readonly_fields(request, obj)
        if obj is None:  # 增加的时候
            return fields

        # 修改的时候
        if fields is None:
            return ("username",)

        fs = list(fields)
        fs.append("username")
        return fs


# 重新注册 user 模块
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
