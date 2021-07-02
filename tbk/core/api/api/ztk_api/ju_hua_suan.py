from typing import Optional, List

from django.http import HttpRequest
from pydantic import BaseModel, Field
from qiyu_api.tbk_api import TbkItemInfo
from qiyu_api.ztk_api import JuHuaSuanArgs

from core.logger import get_logger
from core.resp.base import ResponseModel, ApiResp
from core.vendor.ztk import get_ztk_std_api
from ...api import fields
from ...api.app import app
from ...api_utils import api_inner_wrapper


class JuHuanSuanResponseModel(ResponseModel):
    data: Optional[List[TbkItemInfo]] = Field(None, title="具体信息")


class JuHuaSuanForm(BaseModel):
    """
    聚划算请求参数
    """

    page: int = fields.page_field
    page_size: int = fields.page_size_field
    sort: str = fields.sort_fields
    cid: Optional[int] = fields.cid_field

    def to_data(self) -> JuHuaSuanArgs:
        return JuHuaSuanArgs(**self.dict(by_alias=True))


@app.post(
    "/ztk/ju_hua_suan",
    tags=["折淘客"],
    summary="聚划算",
    description="",
)
async def ju_hua_suan(
    request: HttpRequest, g: JuHuaSuanForm
) -> JuHuanSuanResponseModel:
    logger = get_logger()
    ztk = await get_ztk_std_api(logger)

    @api_inner_wrapper(logger)
    async def inner():
        data = g.to_data()
        j = await ztk.ju_hua_suan(data)
        return ApiResp.from_data(j).to_dict()

    return await inner
