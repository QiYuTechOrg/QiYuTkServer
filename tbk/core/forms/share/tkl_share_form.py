from pydantic import BaseModel, Field

from core.misc import AppFields

__all__ = ["ShareItemTklForm"]


class ShareItemTklForm(BaseModel):
    """
    使用淘口令分享商品的参数
    """

    item_id: str = Field(
        ..., title="淘宝的商品 id", description="都是同一个意思: item_id/num_iid/tao_id"
    )
    token: str = AppFields.token
