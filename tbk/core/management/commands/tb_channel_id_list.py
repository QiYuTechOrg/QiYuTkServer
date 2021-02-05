"""
折淘客 获取绑定的渠道 ID 信息
"""
import asyncio
import sys

from django.core.management.base import BaseCommand, CommandParser

# this is a work around for import error
try:
    from tbk.s_config import SConfig
    from ...api import api
    from ...logger import get_logger
    from ...vendor.ztk import ItemDetailV2Args, ZTK, GaoYongArgs, ChannelIdListArgs
except ImportError as e:
    print(f"导入失败: {e}", file=sys.stderr)
    sys.exit(1)


class Command(BaseCommand):
    help = "获取绑定的渠道 ID 信息"

    def add_arguments(self, parser: CommandParser):
        super().add_arguments(parser)

    def handle(self, *args, **options):
        logger = get_logger()
        args = ChannelIdListArgs(sid=SConfig.ZTKSid, info_type=2)
        ztk = ZTK(logger)
        loop = asyncio.get_event_loop()
        ret = loop.run_until_complete(ztk.channel_id_list(args))
        print(ret)
