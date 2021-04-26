import datetime
import decimal
from typing import List, Optional

from django.http import HttpRequest
from pydantic import BaseModel, Field

from core.api.api import fields
from core.api.api.app import app
from core.api.api_utils import api_inner_wrapper
from core.api.models import dm_fields
from core.logger import get_logger
from core.logic import OrderLogic
from core.models import OrderStatusEnum
from core.resp.base import ResponseModel, ApiResp
from core.shared import OrderType


class OrderListDataModel(BaseModel):
    order_platform: str = dm_fields.order_platform
    order_no: str = dm_fields.order_no
    order_parent_no: str = dm_fields.order_parent_no
    order_num: int = dm_fields.order_num
    order_ctime: datetime.datetime = dm_fields.order_ctime
    order_status: str = dm_fields.order_status
    pay_price: decimal.Decimal = dm_fields.pay_price
    pay_time: Optional[datetime.datetime] = dm_fields.pay_time
    end_time: Optional[datetime.datetime] = dm_fields.end_time
    item_id: str = dm_fields.item_id
    item_title: str = dm_fields.item_title
    item_pic: str = dm_fields.item_pic
    item_price: decimal.Decimal = dm_fields.item_price
    item_category: str = dm_fields.item_category
    shop_title: str = dm_fields.shop_title
    income: decimal.Decimal = dm_fields.income
    score: int = dm_fields.score
    status: str = dm_fields.status
    ctime: datetime.datetime = dm_fields.ctime
    mtime: datetime.datetime = dm_fields.mtime

    def set_status_str(self):
        if self.status == OrderStatusEnum.wait:
            self.status = "等待收货"
        elif self.status == OrderStatusEnum.cancel:
            self.status = "订单已取消"
        elif self.status == OrderStatusEnum.success:
            self.status = "订单已完成"


class OrderListResponseModel(ResponseModel):
    data: Optional[List[OrderListDataModel]] = Field(None, title="详细数据")


class OrderListForm(BaseModel):
    """
    用户信息请求参数
    """

    token: str = fields.token
    page: int = fields.page_field
    typ: OrderType = fields.order_type


@app.post(
    "/order/list",
    tags=["订单"],
    summary="获取订单列表",
)
async def order_list(
    request: HttpRequest, form: OrderListForm
) -> OrderListResponseModel:
    """
    获取用户的淘宝客订单
    """

    logger = get_logger()

    @api_inner_wrapper(logger)
    async def inner():
        ol = OrderLogic(logger)
        data_list = await ol.order_list(form.token, form.typ, form.page)
        ret_list = list(map(lambda x: vars(x), data_list))
        d = ApiResp.from_data(ret_list).to_dict()
        ret = OrderListResponseModel(**d)
        # convert status to str
        for item in ret.data:
            item.set_status_str()
        return ret

    return await inner
