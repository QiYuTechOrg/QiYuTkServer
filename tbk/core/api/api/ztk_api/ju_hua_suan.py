from typing import Optional, List

from fastapi import Depends, Body
from pydantic import BaseModel, Field
from qiyu_api.tbk_api import TbkItemInfo
from qiyu_api.ztk_api import JuHuaSuanArgs, ZTKStd
from structlog.stdlib import BoundLogger

from core.logger import get_logger
from core.resp.base import ResponseModel, ApiResp
from core.vendor.ztk import get_ztk_api_v2
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
        return JuHuaSuanArgs.from_dict(self.dict())


@app.post(
    "/ztk/ju_hua_suan",
    tags=["折淘客"],
    summary="聚划算",
    description="",
    response_model=JuHuanSuanResponseModel,
)
async def ju_hua_suan(
    g: JuHuaSuanForm = Body(..., title="请求参数"),
    logger: BoundLogger = Depends(get_logger),
    ztk: ZTKStd = Depends(get_ztk_api_v2),
):
    @api_inner_wrapper(logger)
    async def inner():
        data = g.to_data()
        j = await ztk.ju_hua_suan(data)
        return ApiResp.from_data(j).to_dict()

    return await inner
