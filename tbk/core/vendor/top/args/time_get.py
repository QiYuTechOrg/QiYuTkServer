from dataclasses import dataclass

from dataclasses_json import DataClassJsonMixin

__all__ = ["TimeGetArgs"]


@dataclass
class TimeGetArgs(DataClassJsonMixin):
    """
    获取淘宝系统当前时间

    doc: https://open.taobao.com/api.htm?docId=120&docType=2
    """

    method: str = "taobao.time.get"
