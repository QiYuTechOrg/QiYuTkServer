"""
折淘客 开放品台 API
"""
from typing import Optional

import structlog
from qiyu_api.ztk_api import ZTKStd

from tbk.s_config import SConfig
from ...logger import get_logger

__all__ = ["get_ztk_api_v2"]


async def get_ztk_api_v2(logger: Optional[structlog.stdlib.BoundLogger] = None):
    if logger is None:
        logger = get_logger()

    sid = await SConfig.async_ztk_sid()
    return ZTKStd(ztk_sid=sid, logger=logger)
