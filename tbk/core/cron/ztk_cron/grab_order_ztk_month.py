from datetime import datetime, timedelta

from apscheduler.schedulers.base import BaseScheduler

from .grab_order_ztk_base import GrabOrderZtkCronBase

__all__ = ["GrabOrderZtkCronMonth"]


class GrabOrderZtkCronMonth(GrabOrderZtkCronBase):
    """
    抓取30天内的订单
    """

    def __init__(self, scheduler: BaseScheduler):
        super().__init__()
        scheduler.add_job(self, "cron", hour=3)

    def _get_query_type(self) -> int:
        return 1

    def _get_start_time(self) -> datetime:
        d = datetime.now() - timedelta(days=30)
        return d
