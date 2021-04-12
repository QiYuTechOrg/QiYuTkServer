from typing import Optional, List

from django.http import HttpRequest
from pydantic import Field
from qiyu_api.dtk_api.gen import TbServiceGetTbServiceResp, TbServiceGetTbServiceArgs

from core.logger import get_logger
from core.resp.base import ResponseModel, ApiResp
from core.shared import AppErrno
from core.vendor.dtk import get_dtk_async
from ...api.app import app
from ...api_utils import api_inner_wrapper


class DtkTbServiceResponseModel(ResponseModel):
    data: Optional[List[TbServiceGetTbServiceResp]] = Field(None, title="详细数据")


@app.post(
    "/dtk/tb_service",
    tags=["大淘客"],
    summary="联盟搜索",
    description="",
    response_model=DtkTbServiceResponseModel,
)
async def dtk_tb_service_get_tb_service(
    request: HttpRequest, args: TbServiceGetTbServiceArgs
):
    logger = get_logger()
    dtk = await get_dtk_async()

    @api_inner_wrapper(logger)
    async def inner():
        j = await dtk.tb_service_get_tb_service(args)
        if j is None:
            return ApiResp.from_errno(AppErrno.dtk_error)
        return ApiResp.from_data(j)

    return await inner
