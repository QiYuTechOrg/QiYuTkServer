from pydantic import BaseModel, Field

__all__ = ["TbkItemDetailForm"]


class TbkItemDetailForm(BaseModel):
    tao_id: str = Field(..., title="淘宝商品ID")
