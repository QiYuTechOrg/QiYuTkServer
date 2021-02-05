class ApiException(Exception):
    pass


class TokenException(ApiException):
    """
    无效的 token
    """

    pass


class TbNotBindException(ApiException):
    """
    当前没有绑定淘宝
    """

    pass


class ZtkException(ApiException):
    """
    请求折淘客失败
    """

    pass


class ItemNotFoundException(ApiException):
    """
    指定的商品没有找到 / 高佣转换失败 等
    """

    pass


class UserNotExistsException(ApiException):
    """
    用户不存在
    """

    pass


class AuthFailedException(ApiException):
    """
    用户认证失败
    """

    pass
