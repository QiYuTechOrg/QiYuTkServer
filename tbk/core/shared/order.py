from enum import IntEnum

__all__ = ["OrderType"]


class OrderType(IntEnum):
    all = 1  # 全部订单
    done = 2  # 已完成
    doing = 3  # 未完成
