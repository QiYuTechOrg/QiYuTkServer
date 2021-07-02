import json
from typing import Awaitable
from urllib.parse import unquote

from asgiref.sync import sync_to_async
from django.contrib.auth.models import User
from qiyu_api.ali_top.args import TopAuthTokenCreateArgs, TBKScPublisherInfoSaveArgs
from qiyu_api.ali_top.sync_api import TopApi
from structlog.stdlib import BoundLogger

from core.models import TBChannelBindModel, TBChannelIdModel
from tbk.s_config import SConfig
from .get_url import GetBindChannelIdUrl

__all__ = ["TaoBaoLogic"]


class TaoBaoLogic(object):
    """
    淘宝相关的操作逻辑
    """

    def __init__(self, logger: BoundLogger):
        self._log = logger

    async def get_bind_channel_id_url(self, token: str) -> dict:
        """
        获取淘宝授权认证的 URL

        正常生成了 state 返回给用户
        @doc https://open.taobao.com/doc.htm?docId=102635&docType=1

        :param token: 用户的 token
        :return: {'url': url}
        """
        logic = GetBindChannelIdUrl(self._log)
        url = await logic.get_bind_channel_id_url(token)
        return {"url": url}

    async def ios_try_bind_v2(self, user: User, code: str) -> bool:
        """
        iOS 版本的尝试绑定渠道 ID

        :param user: 用户
        :param code: 授权的 code
        :return:
        """
        ret = await self._do_ios_bind_async(user, code)
        return ret

    def android_try_bind(self, code: str, state: str) -> bool:
        """
        尝试绑定渠道 ID

        this is a sync function mainly because of this function is used by django

        :return: true 绑定 渠道 ID 成功 false 绑定渠道 ID 失败
        """
        # 获取当前 state 要绑定的用户
        user = TBChannelBindModel.get_user_by_state(state)
        if user is None:
            self._log.bind(state=state).error("invalid state")
            return False

        return self._do_bind(user, code)

    @sync_to_async
    def _do_ios_bind_async(self, user: User, code: str) -> Awaitable[bool]:
        # noinspection PyTypeChecker
        return self._do_bind(user, code)

    def _do_bind(self, user: User, code: str) -> bool:
        # 获取 session key
        # noinspection PyTypeChecker
        top = TopApi(SConfig.AliAppKey, SConfig.AliAppSecret, self._log)
        args = TopAuthTokenCreateArgs(code=code)
        ret = top.top_auth_token_create(args)
        d = json.loads(ret.token_result)
        self._log.bind(token_result=d).info("request session key ok")

        # 保存 用户的昵称
        if "taobao_user_nick" in d:
            nickname = unquote(d["taobao_user_nick"])
            user.profile.nickname = nickname
            user.profile.save()

        # 获取淘宝的头像
        # https://wwc.alicdn.com/avatar/getAvatar.do?userId={userId}&width=160&height=160&type=sns
        if "taobao_user_id" in d:
            user.profile.tao_id = str(d["taobao_user_id"])
            user.profile.save()

        session_key = d["access_token"]

        # 尝试绑定
        return self._do_access_token_bind(session_key, user)

    def _do_access_token_bind(self, access_token: str, user: User):
        # noinspection PyTypeChecker
        top = TopApi(SConfig.AliAppKey, SConfig.AliAppSecret, self._log)

        # 尝试绑定
        invite_code = SConfig.AliInviteCode
        args = TBKScPublisherInfoSaveArgs(
            session=access_token,
            inviter_code=invite_code,
            relation_from="APP",
            note=f"{user.id}",
        )
        ret = top.tbk_sc_publisher_info_save(args)
        self._log.bind(ret=ret).info("bind channel id ok")

        # 保存到数据库中
        TBChannelIdModel.create_or_update(user, ret.relation_id, ret.special_id)
        return True
