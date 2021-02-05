import logging
from logging import Logger
from typing import Optional

import requests

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

__all__ = ["TopApi"]


class TopApi(BaseApi):
    """
    阿里百川 Python SDK Sync Version
    """

    def __init__(self, app_key: str, app_secret: str, logger: Optional[Logger] = None):
        super().__init__(app_key, app_secret)
        self._session = requests.Session()
        self._logger = logging if logger is None else logger

    def user_seller_get(self, args: UserSellerGetArgs):
        url = self._to_url(args.to_dict())
        ret = self._do_request(url)
        print(ret)

    def product_get(self, args: ProductGetArgs):
        url = self._to_url(args.to_dict())
        ret = self._do_request(url)
        print(ret)

    def time_get(self) -> TimeGetResp:
        args = TimeGetArgs()
        ret = self._sync_request(args.to_dict(), args.method)
        return TimeGetResp.from_dict(ret)

    def top_auth_token_create(
        self, args: TopAuthTokenCreateArgs
    ) -> TopAuthTokenCreateResp:
        ret = self._sync_request(args.to_dict(), args.method)
        return TopAuthTokenCreateResp.from_dict(ret)

    def tbk_sc_publisher_info_save(
        self, args: TBKScPublisherInfoSaveArgs
    ) -> TBKScPublisherInfoSaveResp:
        ret = self._sync_request(args.to_dict(), args.method)
        self._logger.info(f"get ret: f{str(ret)}")
        data = ret["data"]
        self._logger.info(f"get data: f{str(data)}")
        return TBKScPublisherInfoSaveResp.from_dict(data)

    def _sync_request(self, args: dict, method: str) -> dict:
        """
        同步发送请求

        抛出的异常:
        TopHttpException, TopErrorRespException

        :param args:
        :param method:
        :return:
        """
        url = self._to_url(args)
        ret = self._do_request(url)
        return self._get_real_data(method, ret)

    def _do_request(self, url: str) -> dict:
        ret = self._session.get(url)
        if ret.ok:
            return ret.json()
        else:
            raise TopHttpException(str(ret))
