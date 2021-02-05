from datetime import datetime, timedelta

from apscheduler.schedulers.base import BaseScheduler

from .grab_order_ztk_base import GrabOrderZtkCronBase

__all__ = ["GrabOrderZtkCronRealPay"]


class GrabOrderZtkCronRealPay(GrabOrderZtkCronBase):
    """
    抓取淘宝实时订单的接口
    """

    def __init__(self, scheduler: BaseScheduler):
        super().__init__()
        scheduler.add_job(self, "interval", seconds=10)

    def _get_query_type(self) -> int:
        return 2  # 付款时间查询

    def _get_start_time(self) -> datetime:
        d = datetime.now() - timedelta(minutes=20)
        return d
