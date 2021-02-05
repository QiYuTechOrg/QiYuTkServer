"""
折淘客 开放品台 API
"""
from typing import Optional

import structlog
from fastapi import Depends
from ztk_api import ZTK

from tbk.s_config import SConfig
from ...logger import get_logger

__all__ = ["get_ztk_api_v2"]

g_ztk: Optional[ZTK] = None


def get_ztk_api_v2(logger: structlog.stdlib.BoundLogger = Depends(get_logger)):
    global g_ztk
    if g_ztk is None:
        g_ztk = ZTK(SConfig.ZTKSid, logger)
    return g_ztk
