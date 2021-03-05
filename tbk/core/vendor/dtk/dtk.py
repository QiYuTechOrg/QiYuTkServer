from typing import Optional

from qiyu_api.dtk_api import DtkAsyncApi, DtkStdApi

from tbk.s_config import SConfig

__all__ = ["get_dtk_async", "get_dtk_std"]

g_dtk: Optional[DtkAsyncApi] = None


async def get_dtk_async() -> DtkAsyncApi:
    global g_dtk
    if g_dtk is None:
        app_key = await SConfig.async_dtk_app_key()
        app_secret = await SConfig.async_dtk_app_secret()
        g_dtk = DtkAsyncApi(app_key, app_secret)
    return g_dtk


g_std: Optional[DtkStdApi] = None


async def get_dtk_std() -> DtkStdApi:
    global g_std
    if g_std is None:
        app_key = await SConfig.async_dtk_app_key()
        app_secret = await SConfig.async_dtk_app_secret()
        g_std = DtkStdApi(app_key=app_key, app_secret=app_secret)
    return g_std
