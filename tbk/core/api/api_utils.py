import traceback
from typing import Callable, Any

from django.contrib.auth.models import User
from django.db import connection
from django.db.utils import InterfaceError
from structlog.stdlib import BoundLogger

from core.excpetions import ApiException
from core.logic import UserV2Logic
from core.resp.base import ApiResp, AppErrno
from .utils import convert_exception_to_api_ret

__all__ = ["api_inner_wrapper", "api_ensure_login"]


def api_ensure_login(token: str, logger: BoundLogger) -> Callable:
    """
    包装 API View 层的逻辑
    确保访问这个接口的用户已经登陆
    """

    async def wrapper(func: Callable[[User], Any]):
        try:
            logic = UserV2Logic(logger)

            user = await logic.get_user_by_token(token)
            if user is None:
                return ApiResp.from_errno(AppErrno.auth_failed).to_dict()

            ret = await func(user)
            if isinstance(ret, ApiResp):
                return ret.to_dict()
            else:
                return ret
        except ApiException as e:
            tb = traceback.format_tb(e.__traceback__)
            logger.bind(exec=e, tb=tb).error("内部处理错误")

            return convert_exception_to_api_ret(e).to_dict()
        except InterfaceError:  # 数据库连接失败
            connection.close()
            logger.error("数据库错误")
            return ApiResp.system_error().to_dict()
        except Exception as e:
            tb = traceback.format_tb(e.__traceback__)
            logger.bind(exce=e, tb=tb).error("其他严重错误")

            return ApiResp.system_error().to_dict()

    return wrapper


def api_inner_wrapper(logger: BoundLogger) -> Callable:
    """
    包装 api view 层的逻辑

    :param logger:
    :return:
    """

    async def wrapper(func: Callable):
        try:
            ret = await func()
            if isinstance(ret, ApiResp):
                return ret.to_dict()
            else:
                return ret
        except ApiException as e:
            tb = traceback.format_tb(e.__traceback__)
            logger.bind(exec=e, tb=tb).error("内部处理错误")
            return convert_exception_to_api_ret(e).to_dict()
        except InterfaceError:  # 数据库连接失败
            connection.close()
            logger.error("数据库错误")
            return ApiResp.system_error().to_dict()
        except Exception as e:
            tb = traceback.format_tb(e.__traceback__)
            logger.bind(exce=e, tb=tb).error("其他严重错误")

            return ApiResp.system_error().to_dict()

    return wrapper
