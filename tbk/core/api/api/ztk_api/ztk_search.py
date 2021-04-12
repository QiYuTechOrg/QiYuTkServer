from typing import Optional, List

from django.http import HttpRequest
from pydantic import BaseModel, Field
from qiyu_api.tbk_api import TbkItemInfo
from qiyu_api.ztk_api import SearchArgs

from core.logger import get_logger
from core.resp.base import ResponseModel, ApiResp
from core.vendor.ztk import get_ztk_api_v2
from ...api import fields
from ...api.app import app
from ...api_utils import api_inner_wrapper


class SearchResponseModel(ResponseModel):
    data: Optional[List[TbkItemInfo]] = Field(None, title="详细数据")


class SearchForm(BaseModel):
    """
    全网搜索
    """

    q: str = Field(..., title="商品标题")

    page: int = fields.page_field
    page_size: int = fields.page_size_field
    sort: str = fields.sort_fields

    youquan: Optional[int] = Field(None, title="是否有券", description="1 为有券，其它值为全部商品")

    def to_data(self) -> SearchArgs:
        return SearchArgs.from_dict(self.dict())


@app.post(
    "/ztk/search",
    tags=["折淘客"],
    summary="全网商品搜索",
    description="",
    response_model=SearchResponseModel,
)
async def ztk_search(request: HttpRequest, f: SearchForm):
    logger = get_logger()
    ztk = get_ztk_api_v2(logger)

    @api_inner_wrapper(logger)
    async def inner():
        data = f.to_data()
        j = await ztk.search(data)
        return ApiResp.from_data(j).to_dict()

    return await inner
