import aiohttp

from .args import (
    UserSellerGetArgs,
    ProductGetArgs,
    TimeGetArgs,
    TopAuthTokenCreateArgs,
    TBKScPublisherInfoSaveArgs,
)
from .base_api import BaseApi
from .exceptions import TopHttpException
from .resp import TimeGetResp, TopAuthTokenCreateResp, TBKScPublisherInfoSaveResp

__all__ = ["AsyncTopApi"]


class AsyncTopApi(BaseApi):
    """
    阿里百川 Python SDK Async Version
    """

    def __init__(self, app_key: str, app_secret: str):
        super().__init__(app_key, app_secret)
        self._session = aiohttp.ClientSession()

    async def user_seller_get(self, args: UserSellerGetArgs):
        url = self._to_url(args.to_dict())
        ret = await self._do_request(url)
        print(ret)

    async def product_get(self, args: ProductGetArgs):
        url = self._to_url(args.to_dict())
        ret = await self._do_request(url)
        print(ret)

    async def time_get(self) -> TimeGetResp:
        args = TimeGetArgs()
        ret = await self._async_request(args.to_dict(), args.method)
        return TimeGetResp.from_dict(ret)

    async def top_auth_token_create(
        self, args: TopAuthTokenCreateArgs
    ) -> TopAuthTokenCreateResp:
        ret = await self._async_request(args.to_dict(), args.method)
        return TopAuthTokenCreateResp.from_dict(ret)

    async def tbk_sc_publisher_info_save(
        self, args: TBKScPublisherInfoSaveArgs
    ) -> TBKScPublisherInfoSaveResp:
        ret = await self._async_request(args.to_dict(), args.method)
        return TBKScPublisherInfoSaveResp.from_dict(ret)

    async def _async_request(self, args: dict, method: str):
        """
        同步发送请求

        抛出的异常:
        TopHttpException, TopErrorRespException

        :param args:
        :param method:
        :return:
        """
        url = self._to_url(args)
        ret = await self._do_request(url)
        return self._get_real_data(method, ret)

    async def _do_request(self, url: str) -> dict:
        ret = await self._session.get(url)
        if 200 <= ret.status < 300:
            return await ret.json()
        else:
            raise TopHttpException(str(ret))
