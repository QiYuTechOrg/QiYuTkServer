from datetime import datetime, timedelta

from apscheduler.schedulers.base import BaseScheduler

from .grab_order_dtk_base import GrabOrderDtkCronBase

__all__ = ["GrabOrderDtkCronHour"]


class GrabOrderDtkCronHour(GrabOrderDtkCronBase):
    """
    抓到淘宝每小时的订单
    """

    def __init__(self, scheduler: BaseScheduler):
        super().__init__()
        scheduler.add_job(self, "interval", minutes=3)

    def _get_query_type(self) -> int:
        return 1

    def _get_start_time(self) -> datetime:
        d = datetime.now() - timedelta(minutes=60)
        return d
