from typing import Optional

from asgiref.sync import async_to_sync
from django.http import HttpRequest
from django.views.generic import TemplateView
from qiyu_api.tbk_api import TbkItemInfo
from qiyu_api.ztk_api import GaoYongArgs
from structlog import get_logger

from core.logic import ZTKLogic
from tbk.s_config import SConfig

__all__ = ["DetailView"]


class DetailView(TemplateView):
    template_name = "tbk/web/detail.html"

    def get_context_data(self, item_id: str, **kwargs):
        assert isinstance(self.request, HttpRequest)
        logger = get_logger("django")

        logic = ZTKLogic(logger)

        args = GaoYongArgs(pid=SConfig.AliPid, num_iid=item_id, sid=SConfig.ZTKSid)

        detail: Optional[TbkItemInfo] = async_to_sync(logic.gao_yong)(args)

        show_coupon = SConfig.WEB_SHOW_COUPON

        return super().get_context_data(detail=detail, show_coupon=show_coupon, **kwargs)
