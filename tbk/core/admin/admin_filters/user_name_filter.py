from django.contrib.admin import ListFilter
from django.db import models
from django.http import HttpRequest

__all__ = ["UsernameFilter"]


class UsernameFilter(ListFilter):
    """
    会过滤 user__username 字段
    """

    title = "用户"
    parameter_name = "username"
    template = "tbk/admin/filters/user_input_filter.html"

    def __init__(self, request: HttpRequest, params, model, model_admin):
        super().__init__(request, params, model, model_admin)

        if self.parameter_name in params:
            value = params.pop(self.parameter_name)
            self.used_parameters[self.parameter_name] = value

    def value(self):
        return self.used_parameters.get(self.parameter_name, None)

    def has_output(self) -> bool:
        return True

    def expected_parameters(self):
        return [self.parameter_name]

    def choices(self, changelist):
        return (
            {
                "get_query": changelist.params,
                "current_value": self.value(),
                "parameter_name": self.parameter_name,
            },
        )

    def queryset(self, request: HttpRequest, queryset: models.QuerySet):
        if self.value():
            return queryset.filter(user__username=self.value())
