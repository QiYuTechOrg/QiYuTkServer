from datetime import datetime, timedelta
from typing import Optional, List
from uuid import uuid4

from django.db import transaction
from qiyu_api.dtk_api import DtkSyncApi
from qiyu_api.dtk_api.gen import TbServiceGetOrderDetailsArgs
from qiyu_api.ztk_api import OrderDetailsResp, OrderDto
from structlog.stdlib import BoundLogger

from core.logger import get_cron_logger
from core.logic import UserV2Logic
from core.models import OrderModel, TBChannelIdModel, OrderStatusEnum
from tbk.s_config import SConfig

__all__ = ["GrabOrderDtkCronBase"]


class GrabOrderDtkCronBase(object):
    """
    基础的抓取淘宝订单的类
    """

    def __init__(self):
        pass

    def __call__(self, *args, **kwargs):
        """
        实时大淘客获取订单处理流程

        :param args:   无用的参数
        :param kwargs: 无用的参数
        :return:
        """
        logger = get_cron_logger()
        logger.bind(name=self.__class__.__name__).info("cron start")

        s = self._get_start_time()
        now = datetime.now()
        query_type = self._get_query_type()

        while s < now:
            plog: BoundLogger = logger.bind(parent=str(uuid4()))
            ret = self._get_order_list(s, query_type, plog)
            order_list = ret.get_order_lists()

            for order in order_list:
                self._process_order(order, plog.bind(uuid=str(uuid4())))

            page = 2
            while True:
                position_index = ret.position_index
                if not ret.has_next:
                    break

                ret = self._get_next_order_list(
                    s, query_type, page, position_index, plog
                )
                page += 1
                order_list = ret.get_order_lists()
                for order in order_list:
                    self._process_order(order, plog.bind(uuid=str(uuid4())))

            s += timedelta(minutes=20)

    def _get_query_type(self) -> int:
        raise NotImplementedError("_get_query_type not impl")

    def _get_start_time(self) -> datetime:
        raise NotImplementedError("_get_start_time not impl")

    def _process_order(self, order: OrderDto, logger: BoundLogger):
        """
        处理一个订单的信息

        :param order: 处理订单
        :return:
        """
        try:
            return self._do_process_order(order, logger)
        except Exception as e:
            logger.bind(exception=e).error("process order failed")

    @transaction.atomic
    def _do_process_order(self, order: OrderDto, logger: BoundLogger):
        """
        执行处理订单的任务

        * 这儿所有的代码都是同步的, 因为是在后台运行, 没有必要使用异步的代码

        :param order: 订单信息
        :param logger: 日志记录器
        :return:
        """
        model = OrderModel.get_by_order_no(order.trade_id)
        if model is None:  # 添加一个新的订单
            return self._do_add_new_order(order, logger)
        else:  # 处理一个老订单
            return self._do_update_old_order(order, model, logger)

    @staticmethod
    def _do_add_new_order(order: OrderDto, logger: BoundLogger):
        """
        添加一个新的订单 [这个 `order` 没有在 订单库中出现过]
        :param order:
        :param logger:
        :return:
        """
        assert order.relation_id is not None
        channel_info: TBChannelIdModel = TBChannelIdModel.get_by_relation_id(
            order.relation_id
        )
        user = channel_info.user

        model: OrderModel = OrderModel(
            user=user,
            order_platform=order.order_platform(),
            order_no=order.trade_id,
            order_parent_no=order.trade_parent_id,
            order_num=order.item_num,
            order_ctime=order.order_ctime(),
            order_status=str(order.tk_status),
            pay_price=order.ali_pay_price(),
            pay_time=order.pay_time(),
            end_time=order.end_time(),
            item_id=str(order.item_id),
            item_title=order.item_title,
            item_pic=order.item_img,
            item_price=order.item_price,
            item_category=order.item_category_name,
            shop_title=order.seller_shop_title,
            income=order.income(),
            score=int(order.income() * 100),
            status=OrderStatusEnum.wait,
            detail=order.dict(by_alias=True),
        )

        # noinspection PyArgumentList
        model.save(force_insert=True)

        if order.is_order_paid():  # 订单已经付款 这是默认的状态 什么都不需要做
            pass
        elif order.is_order_canceled():  # 订单已经取消 这个状态需要重新设置 订单的状态
            model.status = OrderStatusEnum.cancel
        elif order.is_order_success() or order.is_order_done():
            model.status = OrderStatusEnum.success
            event = f"购买: {order.trade_id}"
            logic = UserV2Logic(logger)
            logic.add_score(model.user, event, model.score)

        # noinspection PyArgumentList
        model.save()  # 设置 订单状态为 已经取消

    @staticmethod
    def _do_update_old_order(order: OrderDto, model: OrderModel, logger: BoundLogger):
        """
        更新一个订单信息
        当前的订单信息为 order
        数据库中的信息为 model

        :param order:
        :param model:
        :param logger:
        :return:
        """
        model.order_ctime = order.order_ctime()
        model.order_status = str(order.tk_status)
        model.pay_price = order.ali_pay_price()
        model.pay_time = order.pay_time()
        model.end_time = order.end_time()
        model.income = order.income()
        model.score = (int(order.income() * 100),)
        model.detail = order.dict(by_alias=True)

        if order.is_order_paid():  # 默认状态
            model.status = OrderStatusEnum.wait

        elif order.is_order_canceled():  # 需要查询之前的状态
            if model.status == OrderStatusEnum.wait:
                model.status = OrderStatusEnum.cancel
            elif model.status == OrderStatusEnum.cancel:  # 已经是这个状态 没有必要更新
                pass
            elif model.status == OrderStatusEnum.success:
                logger.bind(order_no=order.trade_id).error("revoke score ?")
                model.status = OrderStatusEnum.cancel

        elif order.is_order_success() or order.is_order_done():
            if model.status == OrderStatusEnum.wait:  # 之前的状态是等待 现在变成 成功状态
                event = f"购买: {order.trade_id}"
                logic = UserV2Logic(logger)
                logic.add_score(model.user, event, int(order.income() * 100))

                model.status = OrderStatusEnum.success
            elif model.status == OrderStatusEnum.cancel:  # 取消之后不可能成功
                logger.bind(order_no=order.trade_id).error("sth impossible happened")
            elif model.status == OrderStatusEnum.success:  # 已经是这个状态 没有必要更新
                pass

        # noinspection PyArgumentList
        model.save()

    def _get_next_order_list(
        self,
        start_time: datetime,
        query_type: int,
        page: int,
        position_index: str,
        logger: BoundLogger,
    ) -> Optional[OrderDetailsResp]:
        """
        获取下一页的订单列表

        :param start_time:
        :param query_type:
        :param page:            必须 > 1
        :param position_index:  必须有
        :param logger:
        :return:
        """
        diff = timedelta(minutes=20)
        end_time = start_time + diff
        s = self._fmt_time(start_time)
        e = self._fmt_time(end_time)
        args = TbServiceGetOrderDetailsArgs(
            startTime=s,
            endTime=e,
            queryType=str(query_type),
            pageNo=str(page),
            positionIndex=position_index,
        )
        return self._do_get_order_list(args, logger)

    def _get_order_list(
        self, start_time: datetime, query_type: int, logger: BoundLogger
    ) -> Optional[OrderDetailsResp]:
        """
        获取订单列表

        :param start_time:
        :param query_type: 参见 NewOrderArgs 的 query_type
        :param logger:
        :return:
        """
        diff = timedelta(minutes=20)
        end_time = start_time + diff
        s = self._fmt_time(start_time)
        e = self._fmt_time(end_time)
        args = TbServiceGetOrderDetailsArgs(
            startTime=s, endTime=e, queryType=str(query_type)
        )
        return self._do_get_order_list(args, logger)

    @staticmethod
    def _do_get_order_list(
        args: TbServiceGetOrderDetailsArgs, logger: BoundLogger
    ) -> Optional[List[dict]]:
        dtk = DtkSyncApi(SConfig.DTKAppKey, SConfig.DTKAppSecret)
        ret_list = dtk.tb_service_get_order_details(args)
        logger.bind(ret_list=ret_list).info("get data")
        return ret_list

    @staticmethod
    def _fmt_time(ne: datetime) -> str:
        return f"{ne.year}-{ne.month}-{ne.day} {ne.hour}:{ne.minute}:{ne.second}"
