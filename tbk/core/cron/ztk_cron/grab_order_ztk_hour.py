from datetime import datetime, timedelta

from apscheduler.schedulers.base import BaseScheduler

from .grab_order_ztk_base import GrabOrderZtkCronBase

__all__ = ["GrabOrderZtkCronHour"]


class GrabOrderZtkCronHour(GrabOrderZtkCronBase):
    """
    抓到淘宝每小时的订单
    """

    def __init__(self, scheduler: BaseScheduler):
        super().__init__()
        scheduler.add_job(self, "interval", minutes=30)

    def _get_query_type(self) -> int:
        return 1

    def _get_start_time(self) -> datetime:
        d = datetime.now() - timedelta(minutes=60)
        return d
