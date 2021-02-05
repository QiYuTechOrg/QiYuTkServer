import asyncio
import os
import sys

from django.core.management.base import BaseCommand, CommandParser
from structlog.stdlib import BoundLogger

from tbk.s_config import SConfig

# this is a work around for import error
try:
    from ...api import api
    from ...logger import get_logger
    from ...vendor.ztk import ItemDetailV2Args, ZTK, GaoYongArgs, BatchItemsArgs
except ImportError:
    sys.exit(1)


def gen_field(k, v) -> str:
    if v is None:
        return f"{k}: Optional[str]"
    else:
        return f"{k}: {v.__class__.__name__}"


def gen_fields(d: dict) -> str:
    fields = []
    for k, v in d.items():
        fields.append(gen_field(k, v))

    return "\n".join(map(lambda x: f"    {x}", fields))


def file_to_content_item_name(f_name: str) -> str:
    """
    convert 'hell_world_resp' to 'HelloWorldContentItem'

    :param f_name:
    :return:
    """
    parts = f_name.split("_")[:-1]

    return "".join(map(lambda x: x.capitalize(), parts)) + "ContentItem"


def file_to_class_name(f_name: str) -> str:
    """
    convert 'hell_world_resp' to 'HelloWorldResp'

    :param f_name:
    :return:
    """
    parts = f_name.split("_")

    return "".join(map(lambda x: x.capitalize(), parts))


def convert_json_to_string(data: dict, name: str):
    fields_code = gen_fields(data)

    t = """# 这个文件是由 json_code_gen_resp.py 自动生成的 请不要修改
from dataclasses import dataclass
from typing import Optional, List, Any

from dataclasses_json import DataClassJsonMixin


@dataclass
class cls_name(DataClassJsonMixin):
""".replace(
        "cls_name", file_to_content_item_name(name)
    )

    t2 = f"""


@dataclass
class {file_to_class_name(name)}(DataClassJsonMixin):
    status: int
    content: List[Any]
"""

    code = t + fields_code + t2

    out = os.path.normpath(
        os.path.join(
            os.path.dirname(__file__), "..", "..", "vendor", "ztk", name + ".py"
        )
    )
    with open(out, "w") as fp:
        print(f"write to file: {out}")
        fp.write(code)


class Command(BaseCommand):
    help = "折淘客代码生成"

    def add_arguments(self, parser: CommandParser):
        super().add_arguments(parser)

    def handle(self, *args, **options):
        self.gen_batch_item()

    def gen_item_detail_v2(self):
        logger = get_logger()
        args = ItemDetailV2Args(tao_id="600106384786", sid=SConfig.ZTKSid)
        ret = self._generic_query(args, logger)
        self._generic_gen_code(ret, "item_detail_v2_resp")

    def gen_gao_yong(self):
        logger = get_logger()
        args = GaoYongArgs(
            num_iid="625543578446",
            pid=SConfig.AliPid,
            sid=SConfig.ZTKSid,
            special_id="2581060384",
        )
        ret = self._generic_query(args, logger)
        self._generic_gen_code(ret, "gao_yong_resp")

    def gen_batch_item(self):
        logger = get_logger()
        args = BatchItemsArgs(num_iids="624458546548")
        ret = self._generic_query(args, logger)
        self._generic_gen_code(ret, "batch_item_resp")

    @staticmethod
    def _generic_query(args, logger: BoundLogger) -> dict:
        """
        :param args:  type is not gao yong args but  GaoYongArgs's BaseArgs
        :param logger:
        :return:
        """
        loop = asyncio.get_event_loop()
        url = loop.run_until_complete(args.to_http_url())
        ztk = ZTK(logger)
        return loop.run_until_complete(ztk.do_query(url))

    @staticmethod
    def _generic_gen_code(ret: dict, name: str):
        assert ret["status"] == 200
        content = ret["content"][0]
        convert_json_to_string(content, name)
