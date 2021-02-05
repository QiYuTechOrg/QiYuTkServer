from dataclasses import dataclass
from typing import List, Dict

from dataclasses_json import DataClassJsonMixin

__all__ = ["UserSellerGetArgs"]


@dataclass
class UserSellerGetArgs(DataClassJsonMixin):
    """
    查询卖家用户信息

    doc: https://open.taobao.com/api.htm?docId=21349&docType=2
    """

    # session key
    session: str

    # 需要返回的字段列表，可选值为返回示例值中的可以看到的字段
    fields: List[str]

    method: str = "taobao.user.seller.get"

    def to_dict(self, **kwargs) -> Dict[str, str]:
        d = super().to_dict(**kwargs)
        d["fields"] = ",".join(d["fields"])
        return d
