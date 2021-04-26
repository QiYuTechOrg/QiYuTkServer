from typing import Optional, List

from django.http import HttpRequest
from pydantic import Field
from qiyu_api.dtk_api.gen import CategoryGetSuperCategoryResp

from core.logger import get_logger
from core.resp.base import ResponseModel, ApiResp
from core.shared import AppErrno
from core.vendor.dtk import get_dtk_async
from ...api.app import app
from ...api_utils import api_inner_wrapper


class DtkSuperCategoryResponseModel(ResponseModel):
    data: Optional[List[CategoryGetSuperCategoryResp]] = Field(None, title="详细数据")


@app.get(
    "/dtk/super_category",
    tags=["大淘客"],
    summary="超级分类",
    description="[大淘客超级分类文档](https://www.dataoke.com/pmc/api-d.html?id=10)",
)
async def dtk_super_category(
    request: HttpRequest,
) -> DtkSuperCategoryResponseModel:
    logger = get_logger()
    dtk = await get_dtk_async()

    @api_inner_wrapper(logger)
    async def inner():
        j = await dtk.category_get_super_category()
        if j is None:
            return ApiResp.from_errno(AppErrno.dtk_error)
        return ApiResp.from_data(j)

    return await inner
