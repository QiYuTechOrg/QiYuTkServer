from typing import Optional, Awaitable

from asgiref.sync import sync_to_async, async_to_sync
from django.core.exceptions import ObjectDoesNotExist
from fastapi import Depends, Body
from pydantic import BaseModel, Field
from structlog.stdlib import BoundLogger
from ztk_api import GaoYongArgs, GaoYongModel

from core.logger import get_logger
from core.logic import ZTKLogic, UserV2Logic
from core.models import TBChannelIdModel
from core.resp.base import ResponseModel, ApiResp
from core.shared import AppErrno
from tbk.s_config import SConfig
from ...api import fields
from ...api.app import app
from ...api_utils import api_inner_wrapper


class GaoYongResponseModel(ResponseModel):
    data: Optional[GaoYongModel] = Field(None, title="详细数据")


class GaoYongForm(BaseModel):
    """
    高佣转链接接口参数
    """

    item_id: str = fields.tao_id_field
    token: str = fields.token

    @staticmethod
    @sync_to_async
    def to_data(
        self: "GaoYongForm", logger: BoundLogger
    ) -> Awaitable[Optional[GaoYongArgs]]:
        logic = UserV2Logic(logger)
        user = async_to_sync(logic.get_user_by_token(self.token))
        if user is None:
            logger.bind(token=self.token).error("user token is invalid")
            # noinspection PyTypeChecker
            return None

        pid = SConfig.AliPid
        sid = SConfig.ZTKSid

        args = GaoYongArgs(num_iid=self.item_id, pid=pid, sid=sid)
        try:
            info = TBChannelIdModel.objects.get(user=user)
            if info.relation_id is not None:
                args.relation_id = info.relation_id
            if info.special_id is not None:
                args.special_id = info.special_id
            # noinspection PyTypeChecker
            return args
        except ObjectDoesNotExist:
            logger.bind(user=user).error("user not bind taobao")
            # noinspection PyTypeChecker
            return args


@app.post(
    "/ztk/gao_yong",
    tags=["折淘客"],
    summary="高佣转链",
    description="",
    response_model=GaoYongResponseModel,
)
async def ztk_gao_yong(
    g: GaoYongForm = Body(..., title="请求参数"), logger: BoundLogger = Depends(get_logger)
):
    @api_inner_wrapper(logger)
    async def init():
        args = await g.to_data(g, logger)
        if args is None:  # 渠道 ID 信息可以没有 [客户端需要判断有渠道 ID 的信息]
            # 在 iOS 上， 因为 iOS 的审核，所以支持不需要 绑定淘宝 也支持购买
            # 在 android 上，必须绑定才允许购买
            return ApiResp.from_errno(AppErrno.no_channel_id)

        logic = ZTKLogic(logger)
        item = await logic.gao_yong(args)
        if item is None:  # 获取数据失败
            logger.error("get gao yong data failed")
            return ApiResp.from_data(None)
        else:
            # 获取数据成功
            return ApiResp.from_data(item)

    return await init
