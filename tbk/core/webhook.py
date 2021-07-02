from typing import Optional

import requests
from structlog.stdlib import get_logger

__all__ = ["send_webhook_request"]


def send_webhook_request(webhook: Optional[str], json_data: dict) -> None:
    """
    发送 WebHook 请求

    :param webhook: WebHook 的地址
    :param json_data: 发送的 data 数据
    """
    if webhook is None or webhook == "":
        return

    logger = get_logger("webhook")
    try:
        resp = requests.post(webhook, json=json_data, timeout=(5.0, 5.0))
        if resp.ok:
            return
        logger.warning(f"send webhook request: {webhook=} failed {resp=}")
    except Exception as e:
        logger.error(f"send webhook request failed with exception: {e=}")
