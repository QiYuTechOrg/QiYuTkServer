from typing import Optional, Awaitable

from asgiref.sync import sync_to_async
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import transaction
from structlog.stdlib import BoundLogger

from core.excpetions import TokenException, TbNotBindException
from core.models import TBChannelIdModel, UserTokenModel

__all__ = ["UserV2Logic"]


class UserV2Logic(object):
    """
    用户的逻辑
    """

    def __init__(self, logger: BoundLogger):
        """
        :param logger: 日志记录器
        """
        self._log = logger

    async def auth(self, username: str, password: str) -> Optional[str]:
        return await sync_to_async(self.do_auth)(username, password)

    def do_auth(self, username: str, password: str) -> Optional[str]:
        user = authenticate(request=None, username=username, password=password)
        if not isinstance(user, User):
            self._log.bind(username=username, password=password).error("login failed")
            return None
        return UserTokenModel.create_or_update(user)

    async def ensure_bind_tb(self, token: str):
        """
        是否绑定了淘宝账号

        :param token: 用户的 token
        :return: None 表示没有找到相关的 token
                 false 表示没有绑定淘宝账号
                 true  表示已经绑定了淘宝账号
        """
        user = await self.get_user_by_token(token)
        await self.get_relation_id(user)

    async def get_relation_by_token(self, token: str) -> int:
        user = await self.get_user_by_token(token)
        return await self.get_relation_id(user)

    async def get_relation_id(self, user: User) -> int:
        """
        获取用户的 relation_id

        :param user:
        :return:
        """
        v: Optional[TBChannelIdModel] = await TBChannelIdModel.get_by_user_async(user)
        if v is None:
            self._log.bind(user=user.id).info("user is not bind")
            raise TbNotBindException()
        if v.relation_id is None:
            self._log.bind(user=user.id).info("user is not bind channel id")
            raise TbNotBindException()
        return int(v.relation_id)

    @transaction.atomic
    def add_score(self, user: User, event: str, delta: int):
        """
        给指定的用户添加积分

        :param user: 用户
        :param event: 事件名称
        :param delta: 积分变更数量
        :return:
        """
        pass

    async def get_user_by_token(self, token: str) -> User:
        """
        根据 token 获取用户的信息

        :param token: 用户的认证令牌
        :return: None 没有找到这个 token
        """
        ret = await UserTokenModel.get_user_by_token_async(token)
        if ret is None:
            self._log.bind(token=token).error("token is invalid")
            raise TokenException()
        return ret

    @sync_to_async
    def cancel_user_account(self, token: str) -> Awaitable[bool]:
        """
        注销用户的账号
        :param token: 用户的认证令牌
        :return:
        """
        # noinspection PyTypeChecker
        return self.do_cancel_user_account(token)

    def do_cancel_user_account(self, token: str) -> bool:
        user_info = UserTokenModel.get_user_by_token(token)
        if user_info is None:
            self._log.bind(token=token).info("token is invalid")
            return False

        # 禁止用户登陆
        # 其他的会由 user 保存的事件触发
        user_info.is_active = False
        user_info.save()

        return True
