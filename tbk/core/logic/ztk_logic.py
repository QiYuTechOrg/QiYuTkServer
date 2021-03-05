from typing import Optional

from qiyu_api.tbk_api import TbkItemInfo
from qiyu_api.ztk_api import GaoYongArgs, ZTKStd
from structlog.stdlib import BoundLogger

from tbk.s_config import SConfig

__all__ = ["ZTKLogic"]


class ZTKLogic(object):
    """
    折淘客逻辑
    """

    def __init__(self, logger: BoundLogger):
        self._log = logger

    async def gao_yong(self, args: GaoYongArgs) -> Optional[TbkItemInfo]:
        """
        高佣转换

        :param args:
        :return:
        """
        ztk = ZTKStd(await SConfig.async_ztk_sid(), self._log)
        ret = await ztk.gao_yong(args)
        return ret
