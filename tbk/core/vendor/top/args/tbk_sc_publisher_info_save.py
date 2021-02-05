from dataclasses import dataclass
from typing import Optional

from dataclasses_json import DataClassJsonMixin

__all__ = ["TBKScPublisherInfoSaveArgs"]


@dataclass
class TBKScPublisherInfoSaveArgs(DataClassJsonMixin):
    """
    淘宝客-公用-私域用户备案

    doc: https://open.taobao.com/api.htm?docId=37988&docType=2
    """

    # 用户登录授权成功后，TOP颁发给应用的授权信息，详细介绍请点击这里。
    # 当此API的标签上注明：“需要授权”，则此参数必传；
    # “不需要授权”，则此参数不需要传；“可选授权”，则此参数为可选
    session: str

    # 渠道备案 - 淘宝客邀请渠道的邀请码
    inviter_code: str

    # 类型，必选 默认为1:
    info_type: int = 1

    # 被调用的目标AppKey，仅当被调用的API为第三方ISV提供时有效
    target_app_key: Optional[str] = None

    # 合作伙伴身份标识
    partner_id: Optional[str] = None

    ###########################################
    # 渠道备案 - 来源，取链接的来源
    relation_from: Optional[str] = None

    # 渠道备案 - 线下场景信息，1 - 门店，2- 学校，3 - 工厂，4 - 其他
    offline_scene: Optional[int] = None

    # 渠道备案 - 线上场景信息，1 - 微信群，2- QQ群，3 - 其他
    online_scene: Optional[int] = None

    # 媒体侧渠道备注
    note: Optional[str] = None

    # 线下备案注册信息,字段包含:
    # 电话号码(phoneNumber，必填)
    # 省(province,必填)
    # 市(city,必填)
    # 区县街道(location,必填)
    # 详细地址(detailAddress,必填)
    # 经营类型(career,线下个人必填)
    # 店铺类型(shopType,线下店铺必填)
    # 店铺名称(shopName,线下店铺必填)
    # 店铺证书类型(shopCertifyType,线下店铺选填)
    # 店铺证书编号(certifyNumber,线下店铺选填)
    register_info: Optional[str] = None

    # 是否采用精简JSON返回格式
    # 仅当format=json时有效，默认值为：false
    simplify: bool = False

    method: str = "taobao.tbk.sc.publisher.info.save"
