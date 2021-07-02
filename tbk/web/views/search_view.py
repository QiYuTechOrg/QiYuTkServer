from asgiref.sync import async_to_sync
from django import forms
from django.http import HttpRequest
from django.shortcuts import redirect
from django.views.generic import TemplateView
from qiyu_api.ztk_api import SearchArgs
from qiyu_api.ztk_api import ZTKStd
from structlog import get_logger

from tbk.s_config import SConfig

__all__ = ["SearchView"]


class SearchForm(forms.Form):
    name = forms.CharField(max_length=255)
    page = forms.IntegerField(required=False, initial=1)


class SearchView(TemplateView):
    template_name = "tbk/web/index.html"

    def get(self, request: HttpRequest, *args, **kwargs):
        logger = get_logger("django")

        form = SearchForm(request.GET)
        if not form.is_valid():
            logger.error(f"form is invalid, {request.GET=}")
            return redirect("/")

        data = form.cleaned_data
        name = data["name"]
        page = data["page"]
        if not isinstance(page, int):
            page = 1
        ztk = ZTKStd(SConfig.ZTKSid, logger=logger)
        args = SearchArgs(q=name, page=page)
        ret = async_to_sync(ztk.search)(args)

        show_coupon = SConfig.WEB_SHOW_COUPON

        return self.render_to_response(
            super().get_context_data(
                data_list=ret, show_coupon=show_coupon, page=page, args=args, form=form, **kwargs
            )
        )
