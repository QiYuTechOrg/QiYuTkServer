from typing import List, Optional, Awaitable

from asgiref.sync import sync_to_async
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils import timezone

from core.shared import OrderType
from .model_utils import MyJsonEncoder

__all__ = ["OrderModel", "OrderStatusEnum"]


# 订单状态枚举值
class OrderStatusEnum(object):
    # 当订单属于这个状态的时候，表示淘宝还没有给我们结算
    wait = "wait"
    # 订单已经失效了[不会给用户增加积分了]
    cancel = "cancel"
    # 订单处理成功【属于这个状态的时候，表示已经增加过积分, 不能再次处理】
    success = "success"


# 订单状态 choices
ORDER_STATUS_CHOICES = (
    (OrderStatusEnum.wait, "等待结算"),
    (OrderStatusEnum.cancel, "已失效"),
    (OrderStatusEnum.success, "已结算"),
)


class OrderModel(models.Model):
    """
    用户淘宝客订单表
    """

    class Meta(object):
        ordering = ("-id",)
        verbose_name = "淘宝客订单"
        verbose_name_plural = "淘宝客订单"
        unique_together = [
            ["order_no", "order_platform"],  # 每个平台的订单号都唯一
        ]

    # 这个订单属于那个用户
    user = models.ForeignKey(
        User,
        db_index=True,
        on_delete=models.DO_NOTHING,
        related_name="orders",
        verbose_name="用户",
        help_text="用户的订单",
    )

    # 交易平台
    order_platform = models.CharField(
        max_length=32, verbose_name="交易平台", help_text="这个订单在那个平台上购买的"
    )

    # 订单号
    order_no = models.CharField(
        max_length=1024, verbose_name="订单号", help_text="在交易平台上的唯一订单号码"
    )

    # 父订单号码
    # 淘宝的一个订单 可以购买多个东西
    # 每个东西的订单号唯一 但是 父订单号不唯一
    # 其它平台 没有则认为是 空
    order_parent_no = models.CharField(
        max_length=1024, default="", verbose_name="父订单号", help_text="在交易平台上的父订单号"
    )

    order_num = models.PositiveIntegerField(
        default=1, verbose_name="商品数量", help_text="这个订单购买的商品数量"
    )

    # 订单创建时间
    order_ctime = models.DateTimeField(
        verbose_name="订单创建时间", help_text="这个订单在平台上的的创建时间"
    )

    # 购买平台订单状态
    order_status = models.CharField(
        choices=(
            ("3", "结算成功"),
            ("12", "订单已付款"),
            ("13", "订单已关闭"),
            ("14", "确认收货"),
        ),
        max_length=32,
        verbose_name="订单状态",
        help_text="订单在平台上的状态 [当前也就是 tk_status 的中文]",
    )

    pay_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="支付价格",
        help_text="用户需要支付的价格 alipay_total_price",
    )

    # 支付时间 没有支付则为 空
    pay_time = models.DateTimeField(
        null=True, verbose_name="订单的支付时间", help_text="这个订单在平台上的支付时间"
    )

    end_time = models.DateTimeField(
        null=True, verbose_name="结算时间", help_text="平台给这个订单的结算时间"
    )

    item_id = models.CharField(
        max_length=128, default="", verbose_name="商品ID", help_text="这个商品在平台上的 ID"
    )

    item_title = models.CharField(
        max_length=1024, verbose_name="商品名称", help_text="购买商品在平台上展示的名称"
    )

    item_pic = models.URLField(
        max_length=2048, verbose_name="商品图片", help_text="这个商品在平台上的图片"
    )

    item_price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="商品价格", help_text="这个商品在平台上的价格"
    )

    item_category = models.CharField(
        max_length=256, default="", verbose_name="商品分类", help_text="这个商品在平台上的分类"
    )

    shop_title = models.CharField(
        max_length=1024, verbose_name="商家名称", help_text="商家在平台上的名称"
    )

    income = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="收入金额",
        help_text="用户购买这一个订单带来的收入 单位: 元",
    )

    # 积分预期增加值
    score = models.PositiveIntegerField(
        verbose_name="积分", help_text="积分预期增加值[也就是这个订单完成后，需要给用户增加多少积分]"
    )

    # 订单状态
    status = models.CharField(
        choices=ORDER_STATUS_CHOICES,
        default=OrderStatusEnum.wait,
        max_length=32,
        verbose_name="状态",
        help_text="订单在咱们自己平台上的状态",
    )

    # 这个订单的详细内容
    # 仅仅作为展示使用 [每次获取订单信息的时候都会更新这个字段]
    detail = models.JSONField(
        encoder=MyJsonEncoder,
        verbose_name="详细内容",
        help_text="订单的详情, 详细的字段解释参见:\nhttps://open.taobao.com/api.htm?docId=43755&docType=2&scopeId=16322",
    )

    # 创建时间
    ctime = models.DateTimeField(
        default=timezone.now, verbose_name="创建时间", help_text="这个订单的创建时间"
    )

    # 修改时间
    mtime = models.DateTimeField(
        auto_now=True, verbose_name="更改时间", help_text="这个订单信息最近的修改时间"
    )

    @staticmethod
    def get_by_order_no(order_no: str) -> Optional["OrderModel"]:
        try:
            return OrderModel.objects.get(order_no=order_no)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    @sync_to_async
    def get_user_order_count_async(user: User, typ: int) -> Awaitable[int]:
        if typ == 2:
            return OrderModel.objects.filter(user=user, pay_time__isnull=False).count()
        elif typ == 3:
            return OrderModel.objects.filter(user=user, pay_time__isnull=True).count()
        else:
            return OrderModel.objects.filter(user=user).count()

    @staticmethod
    @sync_to_async
    def get_page_order_async(
        user: User, typ: OrderType, page: int
    ) -> Awaitable[Optional[List["OrderModel"]]]:
        """
        获取用户指定类型的订单

        :param user: 用户信息
        :param typ: 获取数据的类型
        :param page: 从 1 开始
        :return:
        """
        start = (page - 1) * 10
        end = start + 10
        if typ == OrderType.done:
            return OrderModel.objects.filter(
                user=user, status__in=[OrderStatusEnum.cancel, OrderStatusEnum.success]
            )[start:end:1]
        elif typ == OrderType.doing:
            return OrderModel.objects.filter(
                user=user, status__in=[OrderStatusEnum.wait]
            )[start:end:1]
        else:  # 返回所有的订单
            return OrderModel.objects.filter(user=user)[start:end:1]

    def __str__(self) -> str:
        return f"{self.order_no}({self.user}:{self.item_title})"
