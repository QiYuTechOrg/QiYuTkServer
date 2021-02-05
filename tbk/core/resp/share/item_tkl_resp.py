from typing import Optional

from pydantic import Field

from core.resp.base import ResponseModel

__all__ = ["ShareItemTklResponseModel"]


class ShareItemTklResponseModel(ResponseModel):
    """
    淘口令分享商品的 URL
    """

    data: Optional[str] = Field(
        None, title="淘口令", description="包含淘口令的字符串，可能会包含一些奇奇怪怪的信息"
    )
