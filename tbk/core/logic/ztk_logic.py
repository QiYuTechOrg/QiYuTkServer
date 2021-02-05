from typing import Optional

from structlog.stdlib import BoundLogger
from ztk_api import GaoYongArgs, ZTK, GaoYongModel

from tbk.s_config import SConfig

__all__ = ["ZTKLogic"]


class ZTKLogic(object):
    """
    折淘客逻辑
    """

    def __init__(self, logger: BoundLogger):
        self._log = logger

    async def gao_yong(self, args: GaoYongArgs) -> Optional[GaoYongModel]:
        """
        高佣转换

        :param args:
        :return:
        """
        ztk = ZTK(await SConfig.async_ztk_sid(), self._log)
        ret = await ztk.gao_yong(args)
        if ret.status != 200:
            self._log.bind(ret=ret).error("request ztk failed")
            return None

        if len(ret.content) <= 0:
            self._log.bind(ret=ret).error("request ztk no data")
            return None

        # todo 怎么样找到最好的券 ??
        item = ret.content[0]

        m = GaoYongModel(**item)

        # 当前必须可以没有渠道 ID
        if args.relation_id is not None:
            # have no idea if relationId or relation_id is correct
            rid_str = f"relationId={args.relation_id}&relation_id={args.relation_id}"

            m.item_url = f"{m.item_url}&{rid_str}"
            m.coupon_click_url = f"{m.coupon_click_url}&{rid_str}"

        return m
