from typing import Optional

from qiyu_api.tbk_api import TbkItemInfo
from qiyu_api.ztk_api import GaoYongArgs
from structlog.stdlib import BoundLogger

from core.excpetions import ItemNotFoundException, TbNotBindException
from tbk.s_config import SConfig
from .user_v2 import UserV2Logic
from .ztk_logic import ZTKLogic

__all__ = ["GaoYongLogic"]


class GaoYongLogic(object):
    """
    高佣逻辑
    """

    def __init__(self, logger: BoundLogger):
        self._log = logger

    async def gao_yong(self, item_id: str, token: str) -> Optional[TbkItemInfo]:
        user_logic = UserV2Logic(self._log)
        relation_id = await user_logic.get_relation_by_token(token)
        return await self._do_gao_yong(item_id, str(relation_id))

    async def gao_yong_with_relation_id_optional(
        self, item_id: str, token: str
    ) -> Optional[TbkItemInfo]:
        try:
            return await self.gao_yong(item_id, token)
        except TbNotBindException:
            return await self._do_gao_yong(item_id, None)

    async def _do_gao_yong(
        self, item_id: str, relation_id: Optional[str] = None
    ) -> Optional[TbkItemInfo]:
        """
        高佣分享 可以没有渠道 ID

        :param item_id:
        :param relation_id:
        :return:
        """
        pid = await SConfig.async_ali_pid()
        sid = await SConfig.async_ztk_sid()

        args = GaoYongArgs(num_iid=item_id, pid=pid, sid=sid, relation_id=relation_id)

        logic = ZTKLogic(self._log)
        item = await logic.gao_yong(args)
        if item is None:
            self._log.bind(item_id=item_id).error("gao yong convert failed")
            raise ItemNotFoundException()
        return item
