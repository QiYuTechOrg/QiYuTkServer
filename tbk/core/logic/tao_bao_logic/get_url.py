import secrets
from urllib import parse

from structlog.stdlib import BoundLogger

from core.excpetions import TokenException
from core.models import TBChannelBindModel
from tbk.s_config import SConfig
from .my_utils import get_cb_url
from ..user_logic import UserLogic

__all__ = ["GetBindChannelIdUrl"]


class GetBindChannelIdUrl(object):
    def __init__(self, logger: BoundLogger):
        self._log = logger

    async def get_bind_channel_id_url(self, token: str) -> str:
        """
        获取淘宝授权认证的 URL

        正常生成了 state 返回给用户
        @doc https://open.taobao.com/doc.htm?docId=102635&docType=1

        :param token: 用户的 token
        :return: url
        """
        user = UserLogic(self._log)
        info = await user.get_user_info(token)
        if info is None:
            self._log.error("user is not exists")
            raise TokenException()

        # 保存随机生成的 token 到数据库中
        state = secrets.token_urlsafe(32)
        await TBChannelBindModel.add_or_update_async(info, state)

        # 合成 URL 返回给客户端
        client_id = await SConfig.async_ali_app_key()
        url = "https://oauth.taobao.com/authorize"
        query = parse.urlencode(
            {
                "client_id": client_id,
                "response_type": "code",
                "redirect_uri": get_cb_url(),
                "state": state,
                "view": "wap",
            }
        )

        return f"{url}?{query}"
