from typing import Optional, List

from django.contrib.auth.models import User
from structlog.stdlib import BoundLogger

from core.excpetions import TokenException
from core.models import OrderModel
from core.shared import OrderType
from .user_logic import UserLogic

__all__ = ["OrderLogic"]


class OrderLogic(object):
    """
    订单处理模块
    """

    def __init__(self, logger: BoundLogger):
        """
        日志记录器

        :param logger: 日志
        """
        self._log = logger

    async def order_list(
        self, token: str, typ: OrderType, page: int
    ) -> Optional[List[OrderModel]]:
        """
        获取用户的订单数据列表

        :param token:  用户的 token
        :param typ: 获取数据的类型
        :param page:  获取页面数据: 注意 从 1 开始
        :return:
        """
        user_info = await self._get_user_info(token)
        self._log.bind(user=user_info.username).info("user get order list")
        ret = await OrderModel.get_page_order_async(user_info, typ, page)
        self._log.bind(order_num=len(ret)).info("get order number")
        return ret

    async def order_count(self, token: str, typ: int) -> int:
        """
        获取用户订单数量

        :param token: 用户的 token
        :param typ:  订单类型
        :return:
        """
        user_info = await self._get_user_info(token)

        return await OrderModel.get_user_order_count_async(user_info, typ)

    async def _get_user_info(self, token: str) -> User:
        """
        获取用户的信息 获取失败 抛出 `TokenException` 异常

        :param token: 用户的 token
        :return:
        """
        ul = UserLogic(self._log)
        info = await ul.get_user_info(token)
        if info is None:
            self._log.bind(token=token).error("get user info failed")
            raise TokenException()
        return info
