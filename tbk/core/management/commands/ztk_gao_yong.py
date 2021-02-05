"""
折淘客高佣转链接测试
"""
import asyncio
import sys

from django.core.management.base import BaseCommand, CommandParser

from tbk.s_config import SConfig

# this is a work around for import error
try:
    from ...api import api
    from ...logger import get_logger
    from ...vendor.ztk import ItemDetailV2Args, ZTK, GaoYongArgs
except ImportError:
    sys.exit(1)


class Command(BaseCommand):
    help = "折淘客高佣转换链接"

    def add_arguments(self, parser: CommandParser):
        super().add_arguments(parser)

    def handle(self, *args, **options):
        logger = get_logger()
        args = GaoYongArgs(
            num_iid="625543578446",
            pid=SConfig.AliPid,
            sid=SConfig.ZTKSid,
            special_id="2581060384",
        )
        ztk = ZTK(logger)
        loop = asyncio.get_event_loop()
        ret = loop.run_until_complete(ztk.gao_yong(args))
        print(ret)
