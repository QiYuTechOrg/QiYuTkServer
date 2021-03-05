"""
折淘客 开放品台 API

"""
from typing import Optional

import structlog
from fastapi import Depends
from qiyu_api.ztk_api import ZTKSync

from tbk.s_config import SConfig
from ...logger import get_logger

__all__ = ["get_ztk_sync_api_v2"]

# g is for `global`
g_ztk_sync: Optional[ZTKSync] = None


def get_ztk_sync_api_v2(logger: structlog.stdlib.BoundLogger = Depends(get_logger)):
    global g_ztk_sync
    if g_ztk_sync is None:
        g_ztk_sync = ZTKSync(SConfig.ZTKSid, logger)
    return g_ztk_sync
