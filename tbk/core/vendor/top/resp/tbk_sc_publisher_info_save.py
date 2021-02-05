from dataclasses import dataclass
from typing import Optional

from dataclasses_json import DataClassJsonMixin

__all__ = ["TBKScPublisherInfoSaveResp"]


@dataclass
class TBKScPublisherInfoSaveResp(DataClassJsonMixin):
    """
    淘宝客-公用-私域用户备案

    doc: https://open.taobao.com/api.htm?docId=37988&docType=2
    """

    account_name: str
    desc: str
    relation_id: Optional[int] = None
    special_id: Optional[int] = None
