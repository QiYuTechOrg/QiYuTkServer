from typing import Optional

from asgiref.sync import async_to_sync
from django.http import HttpRequest
from django.views.generic import TemplateView
from qiyu_api.dtk_api.gen import TbServiceGetPrivilegeLinkArgs
from qiyu_api.tbk_api import TbkItemInfo
from qiyu_api.ztk_api import GaoYongArgs
from structlog import get_logger

from core.logic import ZTKLogic
from core.vendor.dtk import get_dtk_std
from tbk.s_config import SConfig

__all__ = ["DetailView"]


class DetailView(TemplateView):
    template_name = "tbk/web/detail.html"

    def get_context_data(self, item_id: str, **kwargs):
        assert isinstance(self.request, HttpRequest)

        show_coupon = SConfig.WEB_SHOW_COUPON

        ztk_detail: Optional[TbkItemInfo] = self._get_ztk_info(item_id=item_id)
        dtk_detail: Optional[TbkItemInfo] = self._get_dtk_info(item_id=item_id)

        if ztk_detail is None and dtk_detail is None:
            detail = None
        elif (
            ztk_detail is None
            or ztk_detail.coupon_link is None
            or ztk_detail.coupon_link == ""
        ):
            detail = dtk_detail
        elif (
            dtk_detail is None
            or dtk_detail.coupon_link is None
            or dtk_detail.coupon_link == ""
        ):
            detail = ztk_detail
        else:
            if float(dtk_detail.commission_money) > float(ztk_detail.commission_money):
                detail = dtk_detail
            else:
                detail = ztk_detail

        return super().get_context_data(
            detail=detail, show_coupon=show_coupon, **kwargs
        )

    @staticmethod
    def _get_ztk_info(item_id: str) -> Optional[TbkItemInfo]:
        logger = get_logger("django")
        logic = ZTKLogic(logger)

        args = GaoYongArgs(pid=SConfig.AliPid, num_iid=item_id, sid=SConfig.ZTKSid)

        return async_to_sync(logic.gao_yong)(args)

    @staticmethod
    @async_to_sync
    async def _get_dtk_info(item_id: str) -> Optional[TbkItemInfo]:
        dtk = await get_dtk_std()

        return await dtk.gao_yong(TbServiceGetPrivilegeLinkArgs(goodsId=item_id))
