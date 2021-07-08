from typing import List

from asgiref.sync import async_to_sync
from django import forms
from django.http import HttpRequest
from django.shortcuts import redirect
from django.views.generic import TemplateView
from qiyu_api.tbk_api import TbkItemInfo
from qiyu_api.ztk_api import SearchArgs, ZTKStd, GaoYongArgs, TKLParseArgs
from structlog import get_logger
from structlog.stdlib import BoundLogger

from tbk.s_config import SConfig

__all__ = ["SearchView"]


class SearchForm(forms.Form):
    name = forms.CharField(max_length=255)
    tkl = forms.CharField(max_length=8, initial=False)
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
        tkl = data["tkl"]
        page = data["page"]
        if not isinstance(page, int):
            page = 1

        sid = SConfig.ZTKSid

        if tkl == "on":
            ali_pid = SConfig.AliPid
            data_list = self.get_data_list_tkl(
                tkl=name, sid=sid, ali_pid=ali_pid, logger=logger
            )
        else:
            data_list = self.get_data_list_search(
                name=name, page=page, sid=sid, logger=logger
            )

        show_coupon = SConfig.WEB_SHOW_COUPON

        return self.render_to_response(
            super().get_context_data(
                data_list=data_list,
                show_coupon=show_coupon,
                page=page,
                args=args,
                form=form,
                tkl=tkl,
                **kwargs,
            )
        )

    @staticmethod
    @async_to_sync
    async def get_data_list_tkl(
        tkl: str, sid: str, ali_pid: str, logger: BoundLogger
    ) -> List[TbkItemInfo]:
        ztk = ZTKStd(sid, logger=logger)
        args = TKLParseArgs(content=tkl, sid=sid)
        tao_id = await ztk.tkl_parse(args)
        if tao_id is None:
            return []

        args = GaoYongArgs(pid=ali_pid, num_iid=tao_id, sid=sid)
        ret = await ztk.gao_yong(args)
        if ret is None:
            return []
        return [ret]

    @staticmethod
    @async_to_sync
    async def get_data_list_search(
        name: str, page: int, sid: str, logger: BoundLogger
    ) -> List[TbkItemInfo]:
        ztk = ZTKStd(sid, logger=logger)
        args = SearchArgs(q=name, page=page)
        data_list = await ztk.search(args)
        return data_list
