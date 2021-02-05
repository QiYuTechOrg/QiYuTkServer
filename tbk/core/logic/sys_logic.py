from structlog.stdlib import BoundLogger

from tbk.s_config import SConfig

__all__ = ["SysLogic"]


class SysLogic(object):
    """
    系统[配置]逻辑
    """

    def __init__(self, logger: BoundLogger):
        self._log = logger

    async def get_sys_config(self) -> dict:
        """
        获取系统配置
        :return:
        """
        pid = await SConfig.async_ali_pid()
        self._log.bind(pid=pid).info("get pid")
        return {"pid": pid}
