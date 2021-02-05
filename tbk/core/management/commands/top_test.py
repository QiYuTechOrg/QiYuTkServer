from django.core.management.base import BaseCommand, CommandParser

from core.vendor.top import TopApi
from tbk.s_config import SConfig


class Command(BaseCommand):
    help = "阿里开放平台 Top测试"

    def add_arguments(self, parser: CommandParser):
        super().add_arguments(parser)

    def handle(self, *args, **options):
        top = TopApi(SConfig.AliAppKey, SConfig.AliAppSecret)
        d = top.time_get()
        print(d)
