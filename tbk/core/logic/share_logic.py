from qiyu_api.ztk_api import ZTK, TKLCreateArgs
from structlog.stdlib import BoundLogger

from core.excpetions import ItemNotFoundException, ZtkException
from tbk.s_config import SConfig
from .gao_yong import GaoYongLogic

__all__ = ["ShareLogic"]


class ShareLogic(object):
    """
    分享商品
    """

    def __init__(self, logger: BoundLogger):
        self._log = logger

    async def ios_share_item(self, item_id: str, token: str, is_ios=False) -> str:
        gao_yong = GaoYongLogic(self._log)
        info = await gao_yong.gao_yong_with_relation_id_optional(item_id, token)
        if info.coupon_link is None:
            self._log.bind(item_id=item_id).error("item is not found")
            raise ItemNotFoundException()
        return await self._do_create_tkl(info.coupon_link, is_ios)

    async def share_item(self, item_id: str, token: str, is_ios=False) -> str:
        """
        分享一个商品

        :param item_id: 要分享的商品 ID
        :param token:  分享的用户 token
        :param is_ios: 是否为 iOS 14 的系统
        :return: 成功返回 淘口令 失败返回 None
        """
        gao_yong = GaoYongLogic(self._log)
        info = await gao_yong.gao_yong(item_id, token)
        if info.coupon_link is None:
            self._log.bind(item_id=item_id).error("item is not found")
            raise ItemNotFoundException()
        return await self._do_create_tkl(info.coupon_link, is_ios)

    async def _do_create_tkl(self, coupon_click_url: str, is_ios: bool = False):
        """

        :param coupon_click_url:
        :param is_ios:  是否为 iOS 14 系统
        :return:
        """
        app_key = await SConfig.async_ali_app_key()
        app_secret = await SConfig.async_ali_app_secret()

        # iOS 14 系统需要特殊的淘口令值
        ty = 1 if is_ios else 0

        args = TKLCreateArgs(
            url=coupon_click_url,
            taobao_appkey=app_key,
            taobao_appsecret=app_secret,
            type=ty,
        )
        ztk = ZTK(await SConfig.async_ztk_sid(), self._log)
        resp = await ztk.tkl_create(args)

        if resp.model is None:
            self._log.bind(resp=resp).error("create tkl failed")
            raise ZtkException()

        return resp.model
