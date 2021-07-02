"""
折淘客 开放品台 API

"""
from typing import Optional

import structlog
from qiyu_api.ztk_api import ZTK

from tbk.s_config import SConfig
from ...logger import get_logger

__all__ = ["get_ztk_api"]


def get_ztk_api(logger: Optional[structlog.stdlib.BoundLogger] = None) -> ZTK:
    if logger is None:
        logger = get_logger()
    return ZTK(SConfig.ZTKSid, logger)
