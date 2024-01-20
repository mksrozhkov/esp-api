# stdlib
import logging.config

# thirdparty
import sentry_sdk
from pythonjsonlogger.jsonlogger import JsonFormatter
from sentry_sdk.integrations.asyncio import AsyncioIntegration
from sentry_sdk.integrations.logging import LoggingIntegration

# project
from src.config import settings


class CustomJsonFormatter(JsonFormatter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.json_ensure_ascii = False


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "format": (
                "%(asctime)s %(levelname)s %(name)s %(module)s %(lineno)s %(message)s"
            ),
            "()": "src.log.CustomJsonFormatter",
            "datefmt": "%Y-%m-%dT%H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "json",
        },
    },
    "loggers": {
        "root": {"handlers": ["console"], "level": "INFO"},
        "uvicorn": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}


def setup_logging():
    if settings.ENVIRONMENT != "dev":
        LOGGING_CONFIG["loggers"]["uvicorn"]["level"] = "WARN"
    logging.config.dictConfig(LOGGING_CONFIG)


def init_sentry():
    sentry_logging = LoggingIntegration(
        level=logging.DEBUG,
        event_level=logging.ERROR,
    )
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        environment=settings.ENVIRONMENT,
        integrations=[
            sentry_logging,
            AsyncioIntegration(),
        ],
        traces_sample_rate=float(settings.TRACES_SAMPLE_RATE),
        max_request_body_size="medium",
    )
