from enum import IntEnum

__all__ = ["AppErrno"]


class AppErrno(IntEnum):
    success = 0

    failure = 1  # 未知的错误
    system = 2  # 系统内部错误

    invalid_user_input = 10

    auth_failed = 11  # 认证失败

    not_found = 20  # 未找到指定内容
    token_invalid = 21  # 无效的 token 客户端应该执行退出 重新登录
    ztk_error = 22  # 折淘客错误
    user_not_exists = 23  # 用户不存在
    dtk_error = 24  # 大淘客错误
    code_error = 25  # 验证码无效
    ali_pay = 26  # 支付宝错误

    release_not_found = 30  # 没有发布的历史

    no_channel_id = 40  # 没有渠道 id 客户端应该 认为 没有绑定淘宝账号 这个时候自动退出

    item_not_found = 41  # 没有找到指定的商品

    def __str__(self) -> str:
        d = {
            AppErrno.success: "成功",
            AppErrno.failure: "未知的错误",
            AppErrno.system: "系统内部错误",
            AppErrno.invalid_user_input: "无效的用户名或者密码",
            AppErrno.auth_failed: "认证失败",
            AppErrno.not_found: "没有找到指定的内容",
            AppErrno.token_invalid: "无效的 token",
            AppErrno.ztk_error: "折淘客错误",
            AppErrno.user_not_exists: "用户不存在",
            AppErrno.dtk_error: "大淘客错误",
            AppErrno.code_error: "验证码错误或者已经失效",
            AppErrno.ali_pay: "请求支付宝失败",
            AppErrno.release_not_found: "没有APP发布记录",
            AppErrno.no_channel_id: "没有找到渠道 id 信息",
            AppErrno.item_not_found: "没有找到指定商品的优惠信息",
        }

        return d.get(self, "未知的错误码")
