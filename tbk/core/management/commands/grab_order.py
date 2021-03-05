from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.schedulers.blocking import BlockingScheduler
from django.core.management.base import BaseCommand, CommandParser

from core.cron.dtk_cron import *  # noqa


class Command(BaseCommand):
    help = "运行定时任务 包含: 抓取订单 删除无用设备 等等"

    def add_arguments(self, parser: CommandParser):
        super().add_arguments(parser)

    def handle(self, *args, **options):
        """
        处理实时获取订单
        """
        job_stores = {"default": MemoryJobStore()}
        executors = {
            "default": ThreadPoolExecutor(10),
        }

        bs = BlockingScheduler(job_stores=job_stores, executors=executors)

        # 添加指定的任务
        # todo dtk 订单抓取
        GrabOrderDtkCronHour(bs)  # noqa

        # 启动处理
        bs.start()
