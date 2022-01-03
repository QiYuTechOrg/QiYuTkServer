from typing import List

from django.http import HttpRequest
from qiyu_api.tbk_api import TbkItemInfo
from qiyu_api.ztk_api import GuessYouLikeArgs

args: GuessYouLikeArgs

data_list: List[TbkItemInfo]

show_coupon: bool  # 是否显示优惠信息

page: int  # 页数

request: HttpRequest
