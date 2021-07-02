import json
import logging.config
import os
from uuid import uuid4

import structlog
from structlog.stdlib import BoundLogger

__all__ = [
    "get_logger",
    "get_django_logger",
    "get_error_logger",
    "get_event_logger",
    "get_cron_logger",
    "get_time_logger",
    "get_api_logger",
    "get_file_logger",
]


def log_file_path(filename: str) -> str:
    return os.path.join(os.path.dirname(__file__), "", "..", "..", "logs", filename)


def my_json_serialize(obj, **kwargs):
    kwargs.pop("ensure_ascii", None)  # pop if exists
    return json.dumps(obj, ensure_ascii=False, **kwargs)


backupCount = 100

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "handlers": {
        "api": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "level": "INFO",
            "filename": log_file_path("api.log"),
            "utc": False,
            "when": "d",
            "backupCount": backupCount,
        },
        "cron": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "level": "DEBUG",
            "filename": log_file_path("cron.log"),
            "utc": False,
            "when": "d",
            "backupCount": backupCount,
        },
        "django": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "level": "DEBUG",
            "filename": log_file_path("django.log"),
            "utc": False,
            "when": "d",
            "backupCount": 10,
        },
        "error": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "level": "INFO",
            "filename": log_file_path("error.log"),
            "utc": False,
            "when": "d",
            "backupCount": backupCount,
        },
        "event": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "level": "DEBUG",
            "filename": log_file_path("event.log"),
            "utc": False,
            "when": "d",
            "backupCount": backupCount,
        },
        "webhook": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "level": "DEBUG",
            "filename": log_file_path("webhook.log"),
            "utc": False,
            "when": "d",
            "backupCount": backupCount,
        },
        "file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "level": "INFO",
            "filename": log_file_path("file.log"),
            "utc": False,
            "when": "d",
            "backupCount": backupCount,
        },
        "root": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "level": "INFO",
            "filename": log_file_path("root.log"),
            "utc": False,
            "when": "d",
            "backupCount": backupCount,
        },
        "time": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "level": "DEBUG",
            "filename": log_file_path("time.log"),
            "utc": False,
            "when": "d",
            "backupCount": backupCount,
        },
    },
    "loggers": {
        "api": {"handlers": ["api"], "propagate": False},
        "cron": {"handlers": ["cron"], "propagate": False},
        "django": {"handlers": ["django"], "propagate": False},
        "error": {"handlers": ["error"], "propagate": False},
        "event": {"handlers": ["event"], "propagate": False},
        "webhook": {"handlers": ["webhook"], "propagate": False},
        "file": {"handlers": ["file"], "propagate": False},
        "time": {"handlers": ["time"], "propagate": False},
    },
    "root": {"handlers": ["root"], "level": "INFO"},
}

logging.config.dictConfig(LOGGING)

# noinspection PyTypeChecker
structlog.configure(
    processors=[
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S", utc=False),
        structlog.processors.JSONRenderer(serializer=my_json_serialize),
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)


def get_cron_logger() -> BoundLogger:
    return structlog.get_logger("cron", root=str(uuid4()))


def get_logger() -> BoundLogger:
    """
    获取日志的辅助函数

        注意:
        返回的类型并不是真正的 `structlog.stdlib.BoundLogger`
        而是 `structlog.stdlib.BoundLogger` 类型的代理
        这儿写返回这个类型仅仅是为了 代码自动补全以及 IDE 的智能分析功能

    注意:
        django-structlog 依赖 structlog
        structlog 使用了 thread local 数据结构
        如果迁移到 异步的 view 可能会有问题

    :return: struct log 记录器
    """
    return structlog.get_logger("api", uuid=str(uuid4()))


def get_django_logger() -> BoundLogger:
    return structlog.get_logger("django", uuid=str(uuid4()))


def get_time_logger() -> BoundLogger:
    return structlog.get_logger("time")


def get_error_logger() -> BoundLogger:
    return structlog.get_logger("error")


def get_file_logger() -> BoundLogger:
    return structlog.get_logger("file")


def get_api_logger() -> BoundLogger:
    return structlog.get_logger("api")


def get_event_logger() -> BoundLogger:
    return structlog.get_logger("event")
