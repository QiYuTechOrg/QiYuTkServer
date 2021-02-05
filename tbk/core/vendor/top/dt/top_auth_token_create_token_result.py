from dataclasses import dataclass

from dataclasses_json import DataClassJsonMixin

__all__ = ["TopAuthTokenCreateTokenResult"]


@dataclass
class TopAuthTokenCreateTokenResult(DataClassJsonMixin):
    w1_expires_in: int
    refresh_token_valid_time: int
    taobao_user_nick: str
    re_expires_in: int
    expire_time: int
    open_uid: str
    token_type: str
    access_token: str
    taobao_open_uid: str
    w1_valid: int
    refresh_token: str
    w2_expires_in: int
    w2_valid: int
    r1_expires_in: int
    r2_expires_in: int
    r2_valid: int
    r1_valid: int
    expires_in: int
