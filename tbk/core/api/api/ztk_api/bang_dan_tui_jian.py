from typing import Optional, List

from django.http import HttpRequest
from pydantic import BaseModel, Field
from qiyu_api.tbk_api import TbkItemInfo
from qiyu_api.ztk_api import BangDanTuiJianArgs

from core.logger import get_logger
from core.resp.base import ResponseModel, ApiResp
from core.vendor.ztk import get_ztk_api_v2
from ...api import fields
from ...api.app import app
from ...api_utils import api_inner_wrapper


class BangDanTuiJianResponseModel(ResponseModel):
    data: Optional[List[TbkItemInfo]] = Field(None, title="详细数据")


class BangDanTuiJianForm(BaseModel):
    """
    榜单推荐请求参数
    """

    page: int = fields.page_field
    page_size: int = fields.page_size_field
    sort: str = fields.sort_fields
    cid: Optional[int] = fields.cid_field

    def to_data(self) -> BangDanTuiJianArgs:
        return BangDanTuiJianArgs(**self.dict())


@app.post(
    "/ztk/bang_dan_tui_jian",
    tags=["折淘客"],
    summary="榜单推荐",
    description="",
)
async def bang_dan_tui_jian(
    request: HttpRequest, g: BangDanTuiJianForm
) -> BangDanTuiJianResponseModel:
    logger = get_logger()
    ztk = get_ztk_api_v2(logger)

    @api_inner_wrapper(logger)
    async def inner():
        data = g.to_data()
        j = await ztk.bang_dan_tui_jian(data)
        return ApiResp.from_data(j).to_dict()

    return await inner
