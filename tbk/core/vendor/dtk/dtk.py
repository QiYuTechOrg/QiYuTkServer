from qiyu_api.dtk_api import DtkAsyncApi, DtkStdApi

from tbk.s_config import SConfig

__all__ = ["get_dtk_async", "get_dtk_std"]


async def get_dtk_async() -> DtkAsyncApi:
    app_key = await SConfig.async_dtk_app_key()
    app_secret = await SConfig.async_dtk_app_secret()
    return DtkAsyncApi(app_key, app_secret)


async def get_dtk_std() -> DtkStdApi:
    app_key = await SConfig.async_dtk_app_key()
    app_secret = await SConfig.async_dtk_app_secret()
    return DtkStdApi(app_key=app_key, app_secret=app_secret)
