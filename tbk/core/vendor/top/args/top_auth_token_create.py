from dataclasses import dataclass
from typing import Optional

from dataclasses_json import DataClassJsonMixin

__all__ = ["TopAuthTokenCreateArgs"]


@dataclass
class TopAuthTokenCreateArgs(DataClassJsonMixin):
    """
    获取Access Token

    doc: https://open.taobao.com/api.htm?docId=25388&docType=2
    """

    code: str  # 授权code，grantType==authorization_code 时需要

    uuid: Optional[str] = None  # 与生成code的uuid配对

    method: str = "taobao.top.auth.token.create"
