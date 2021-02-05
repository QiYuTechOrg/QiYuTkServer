from dataclasses import dataclass
from typing import List, Dict, Optional

from dataclasses_json import DataClassJsonMixin

__all__ = ["ProductGetArgs"]


@dataclass
class ProductGetArgs(DataClassJsonMixin):
    """
    获取一个产品的信息

    doc: https://open.taobao.com/api.htm?docId=4&docType=2
    """

    # Product的id.两种方式来查看一个产品:
    # 1.传入product_id来查询
    # 2.传入cid和props来查询
    product_id: Optional[int] = None

    # 商品类目id.
    # 调用taobao.itemcats.get获取;
    # 必须是叶子类目id,
    # 如果没有传product_id,那么cid和props必须要传.
    cid: Optional[int] = None

    # 比如:诺基亚N73这个产品的关键属性列表就是:
    # 品牌:诺基亚;型号:N73,对应的PV值就是10005:10027;10006:29729.
    props: Optional[int] = None

    method: str = "taobao.product.get"

    # 需要返回的字段列表，可选值为返回示例值中的可以看到的字段
    fields: List[str] = ("name", "binds", "product_id")

    def to_dict(self, **kwargs) -> Dict[str, str]:
        d = super().to_dict(**kwargs)
        d["fields"] = ",".join(d["fields"])
        return d
