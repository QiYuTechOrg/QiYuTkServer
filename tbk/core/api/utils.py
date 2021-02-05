from core.excpetions import (
    ApiException,
    TokenException,
    UserNotExistsException,
    TbNotBindException,
    ItemNotFoundException,
    ZtkException,
    AuthFailedException,
)
from core.resp.base import ApiResp
from core.shared import AppErrno

__all__ = ["convert_exception_to_api_ret"]


def convert_exception_to_api_ret(e: ApiException) -> ApiResp:
    """
    把异常转换成错误的返回值

    :param e:
    :return:
    """
    if isinstance(e, TokenException):
        return ApiResp.from_errno(AppErrno.token_invalid, "您的认证凭证已经 过期/失效 ,请尝试重新登录")
    elif isinstance(e, UserNotExistsException):
        return ApiResp.from_errno(AppErrno.user_not_exists, "账号不存在")
    elif isinstance(e, TbNotBindException):
        return ApiResp.from_errno(AppErrno.no_channel_id, "没有淘宝授权")
    elif isinstance(e, ItemNotFoundException):
        return ApiResp.from_errno(AppErrno.item_not_found, "没有找到指定商品的优惠信息")
    elif isinstance(e, AuthFailedException):
        return ApiResp.from_errno(AppErrno.code_error, "验证码错误或者已经失效")
    elif isinstance(e, ZtkException):
        return ApiResp.from_errno(AppErrno.ztk_error, "请求第三方接口失败, 请稍后再试")
    else:
        return ApiResp.from_errno(AppErrno.system, "系统内部错误")
