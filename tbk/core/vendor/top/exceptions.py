__all__ = ["TopHttpException", "TopErrorRespException"]


class TopHttpException(Exception):
    """
    网络错误/HTTP请求错误
    """

    def __init__(self, msg: str):
        super().__init__()
        self._msg = msg


class TopErrorRespException(Exception):
    """
    返回的结果错误 缺少权限等
    """

    def __int__(self, ret: dict):
        super().__init__()
        self._ret = ret
