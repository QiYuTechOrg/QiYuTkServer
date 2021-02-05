from typing import Optional, List

from pydantic import Field
from tbk_api import TbkItemInfo

from core.resp.base import ResponseModel

__all__ = ["GenericItemListResponseModel"]


class GenericItemListResponseModel(ResponseModel):
    """
    通用商品列表返回
    """

    data: Optional[List[TbkItemInfo]] = Field(None, title="详细数据")
