import hashlib
from datetime import datetime
from urllib import parse

from .exceptions import TopErrorRespException

__all__ = ["BaseApi"]


class BaseApi(object):
    """
    阿里百川 Python SDK
    """

    base_url = "https://eco.taobao.com/router/rest"

    def __init__(self, app_key: str, app_secret: str):
        """
        淘宝开放平台 API

        :param app_key:
        :param app_secret:
        """
        self._app_key = app_key
        self._app_secret = app_secret

    @staticmethod
    def _get_real_data(method: str, d: dict) -> dict:
        parts = method.split(".")[1:]
        key = "_".join(parts) + "_response"
        if key in d:
            return d[key]
        raise TopErrorRespException(d)

    def _to_url(self, d: dict) -> str:
        """
        转换成需要请求的 URL

        :param d: 请求的参数
        :return:
        """
        data = self._to_data(d)
        query = parse.urlencode(data)
        return f"{self.base_url}?{query}"

    def _to_data(self, d: dict) -> dict:
        d["app_key"] = self._app_key
        d["format"] = "json"
        d["v"] = "2.0"
        d["sign_method"] = "md5"
        t = datetime.now()
        d[
            "timestamp"
        ] = f"{t.year:04}-{t.month:02}-{t.day:02} {t.hour:02}:{t.minute:02}:{t.second:02}"

        # remove none value
        n = {k: v for k, v in d.items() if v is not None}

        sign = self._create_sign(n, self._app_secret)
        n["sign"] = sign
        return n

    @staticmethod
    def _create_sign(d: dict, secret: str):
        """
        copy from https://open.taobao.com/doc.htm?docId=131&docType=1

        :param d:
        :param secret:
        :return:
        """
        k = d.keys()
        k = sorted(k)

        sign = secret
        for key in k:
            value = d[key]
            if key != "" and value != "":
                sign = f"{sign}{key}{value}"
        sign = f"{sign}{secret}"

        d = hashlib.md5(sign.encode())

        return d.hexdigest().upper()
