"""
折淘客 开放品台 API

"""
from typing import Optional

import structlog
from qiyu_api.ztk_api import ZTKSync

from tbk.s_config import SConfig
from ...logger import get_logger

__all__ = ["get_ztk_sync_api_v2"]


def get_ztk_sync_api_v2(logger: Optional[structlog.stdlib.BoundLogger] = None):
    if logger is None:
        logger = get_logger()
    return ZTKSync(SConfig.ZTKSid, logger)
