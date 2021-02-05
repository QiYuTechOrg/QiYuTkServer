from typing import Optional

from asgiref.sync import sync_to_async
from django.contrib.auth.models import User
from structlog.stdlib import BoundLogger

from core.dm.user import UserProfileDataModel
from core.models import UserTokenModel, TBChannelIdModel

__all__ = ["UserLogic"]


class UserLogic(object):
    """
    用户处理逻辑
    """

    def __init__(self, logger: BoundLogger):
        self._log = logger

    async def get_user_info(self, token: str) -> Optional[User]:
        """
        根据 *token* 获取用户的信息

        :param token: 用户的口令
        :return:
        """
        ret = await UserTokenModel.get_user_by_token_async(token)
        if ret is None:
            self._log.bind(token=token).error("token is invalid, not exists user")
            return None
        return ret

    async def profile(self, user: User) -> UserProfileDataModel:
        """
        获取用户的基本信息
        :param user:
        :return:
        """
        return await sync_to_async(self._do_get_profile)(user)

    @staticmethod
    def _do_get_profile(user: User) -> UserProfileDataModel:
        channel = TBChannelIdModel.get_by_user(user)
        relation_id = None if channel is None else channel.relation_id
        profile = user.profile
        data = UserProfileDataModel(
            mobile=profile.mobile,
            tao_id=profile.tao_id,
            wx=profile.wx,
            relation_id=relation_id,
        )
        return data
