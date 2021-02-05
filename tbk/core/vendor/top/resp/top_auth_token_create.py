from dataclasses import dataclass

from dataclasses_json import DataClassJsonMixin

__all__ = ["TopAuthTokenCreateResp"]


@dataclass
class TopAuthTokenCreateResp(DataClassJsonMixin):
    """
    获取Access Token

    doc: https://open.taobao.com/api.htm?docId=25388&docType=2
    """

    """
    返回的是json信息
    和之前调用
    https://oauth.taobao.com/tac/token
    https://oauth.alibaba.com/token
    换token返回的字段信息一致

    参见: dt.TopAuthTokenCreateTokenResult
    """
    token_result: str
