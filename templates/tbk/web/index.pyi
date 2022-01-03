from typing import List, Optional

from django.http import HttpRequest
from qiyu_api.tbk_api import TbkItemInfo
from qiyu_api.ztk_api import GuessYouLikeArgs

args: GuessYouLikeArgs

data_list: List[TbkItemInfo]

show_coupon: bool  # 是否显示优惠信息

page: int  # 页数

name: Optional[str]  # 搜索名称

tkl: bool  # 是否为淘口令

request: HttpRequest
