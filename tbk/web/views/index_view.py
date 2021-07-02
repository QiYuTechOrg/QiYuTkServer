from asgiref.sync import async_to_sync
from django.http import HttpRequest
from django.views.generic import TemplateView
from qiyu_api.ztk_api import ZTKStd, GuessYouLikeArgs
from structlog import get_logger

from tbk.s_config import SConfig

__all__ = ["IndexView"]


class IndexView(TemplateView):
    template_name = "tbk/web/index.html"

    def get_context_data(self, **kwargs):
        page = int(self.request.GET.get("page", 1))

        assert isinstance(self.request, HttpRequest)
        logger = get_logger("django")

        args = GuessYouLikeArgs(**self.request.GET.dict())  # noqa

        ztk = ZTKStd(SConfig.ZTKSid, logger)
        ret = async_to_sync(ztk.guess_you_like)(args)

        show_coupon = SConfig.WEB_SHOW_COUPON

        return super().get_context_data(
            data_list=ret, show_coupon=show_coupon, page=page, args=args, **kwargs
        )
