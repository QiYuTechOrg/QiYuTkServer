import traceback
from dataclasses import dataclass
from typing import Optional

from dataclasses_json import DataClassJsonMixin
from django import forms
from django.http import HttpRequest
from django.views.generic import TemplateView

from core.logger import get_logger
from core.logic import TaoBaoLogic

__all__ = ["TaoBaoCB"]


@dataclass
class TaoBaoCbData(DataClassJsonMixin):
    code: str
    state: str


class TaoBaoCbForm(forms.Form):
    code = forms.CharField(max_length=256)
    state = forms.CharField(max_length=128)

    def to_data(self) -> Optional[TaoBaoCbData]:
        if self.is_valid():
            return TaoBaoCbData.from_dict(self.cleaned_data)
        return None


class TaoBaoCB(TemplateView):
    """
    绑定渠道 ID 回调
    """

    template_name = "tbk/taobao/cb.html"

    def get(self, request: HttpRequest, *args, **kwargs):
        logger = get_logger()
        logger.bind(get=request.GET).info("cb GET data")

        form = TaoBaoCbForm(request.GET)
        data = form.to_data()
        logger.bind(data=data).info("cb parsed data")

        if data is None:
            return self.render_to_response({"success": False})

        logic = TaoBaoLogic(logger)
        try:
            ret = logic.android_try_bind(data.code, data.state)
            if ret:
                ctx = {"success": True}
            else:
                ctx = {"success": False}
            return self.render_to_response(ctx)
        except Exception as e:
            tb = traceback.extract_tb(e.__traceback__)
            logger.bind(tb=tb, exce=e).error("内部处理错误")

            ctx = {"success": False}
            return self.render_to_response(ctx)
