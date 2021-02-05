from typing import List, Optional

from fastapi import Depends
from fastapi import Query
from pydantic import Field
from structlog.stdlib import BoundLogger
from ztk_api import ZTK, SuggestArgs

from core.logger import get_logger
from core.resp.base import ApiResp, ResponseModel
from core.vendor.ztk import get_ztk_api_v2
from ...api.app import app
from ...api_utils import api_inner_wrapper


class SuggestResponseModel(ResponseModel):
    data: Optional[List[str]] = Field(None, title="推荐词")


@app.get(
    "/ztk/suggest",
    tags=["折淘客"],
    summary="关键词推荐",
    description="",
    response_model=SuggestResponseModel,
)
async def ztk_suggest(
    content: str = Query(..., title="搜索关键词"),
    logger: BoundLogger = Depends(get_logger),
    ztk: ZTK = Depends(get_ztk_api_v2),
):
    @api_inner_wrapper(logger)
    async def inner():
        args = SuggestArgs(content=content)
        j = await ztk.suggest(args)
        return ApiResp.from_data(j).to_dict()

    return await inner
