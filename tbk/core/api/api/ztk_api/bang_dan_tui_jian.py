from typing import Optional, List

from fastapi import Depends, Body
from pydantic import BaseModel, Field
from structlog.stdlib import BoundLogger
from ztk_api import ZTK, BangDanTuiJianArgs, BangDanTuiJianModel

from core.logger import get_logger
from core.resp.base import ResponseModel, ApiResp
from core.vendor.ztk import get_ztk_api_v2
from ...api import fields
from ...api.app import app
from ...api_utils import api_inner_wrapper


class BangDanTuiJianResponseModel(ResponseModel):
    data: Optional[List[BangDanTuiJianModel]] = Field(None, title="详细数据")


class BangDanTuiJianForm(BaseModel):
    """
    榜单推荐请求参数
    """

    page: int = fields.page_field
    page_size: int = fields.page_size_field
    sort: str = fields.sort_fields
    cid: Optional[int] = fields.cid_field

    def to_data(self) -> BangDanTuiJianArgs:
        return BangDanTuiJianArgs.from_dict(self.dict())


@app.post(
    "/ztk/bang_dan_tui_jian",
    tags=["折淘客"],
    summary="榜单推荐",
    description="",
    response_model=BangDanTuiJianResponseModel,
)
async def bang_dan_tui_jian(
    g: BangDanTuiJianForm = Body(..., title="请求参数"),
    logger: BoundLogger = Depends(get_logger),
    ztk: ZTK = Depends(get_ztk_api_v2),
):
    @api_inner_wrapper(logger)
    async def inner():
        data = g.to_data()
        j = await ztk.bang_dan_tui_jian(data)
        return ApiResp.from_data(j.content).to_dict()

    return await inner
