from pydantic import BaseModel, Field

__all__ = ["TbkBrandListForm", "TbkBrandGoodsForm"]


class TbkBrandListForm(BaseModel):
    page_id: int = Field(1, title="获取第几页数据")


class TbkBrandGoodsForm(BaseModel):
    brand_id: str = Field(..., title="品牌ID")
    page_id: int = Field(1, title="获取第几页数据")
