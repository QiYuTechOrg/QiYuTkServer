from datetime import datetime, timedelta

from apscheduler.schedulers.base import BaseScheduler

from .grab_order_ztk_base import GrabOrderZtkCronBase

__all__ = ["GrabOrderZtkCronDay"]


class GrabOrderZtkCronDay(GrabOrderZtkCronBase):
    """
    抓取淘宝每天的订单
    """

    def __init__(self, scheduler: BaseScheduler):
        super().__init__()
        scheduler.add_job(self, "interval", hours=8)

    def _get_query_type(self) -> int:
        return 1

    def _get_start_time(self) -> datetime:
        d = datetime.now() - timedelta(hours=24)
        return d
