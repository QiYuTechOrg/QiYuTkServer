import asyncio
import sys

from django.core.management.base import BaseCommand, CommandParser

from tbk.s_config import SConfig

# this is a work around for import error
try:
    from ...api import api
    from ...logger import get_logger
    from ...vendor.ztk import (
        ItemDetailV2Args,
        ZTK,
        GaoYongArgs,
        TKLCreateArgs,
        GaoYongResp,
        GaoYongModel,
        TKLCreateResp,
    )
except ImportError:
    sys.exit(1)


class Command(BaseCommand):
    help = "折淘客 淘口令创建 iOS 14 版本测试"

    def add_arguments(self, parser: CommandParser):
        super().add_arguments(parser)

    def handle(self, *args, **options):
        logger = get_logger()
        args = GaoYongArgs(
            num_iid="565894850909", pid=SConfig.AliPid, sid=SConfig.ZTKSid
        )
        ztk = ZTK(logger)
        loop = asyncio.get_event_loop()
        ret: GaoYongResp = loop.run_until_complete(ztk.gao_yong(args))
        assert ret.status == 200

        c = ret.content[0]
        model = GaoYongModel(**c)

        tkl_args = TKLCreateArgs(
            url=model.item_url,
            taobao_appkey=SConfig.AliAppKey,
            taobao_appsecret=SConfig.AliAppSecret,
            type=1,
        )

        ret: TKLCreateResp = loop.run_until_complete(ztk.tkl_create(tkl_args))
        print(ret.model)
